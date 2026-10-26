import os
import subprocess
import shutil
import asyncio
import logging
import unicodedata
import imageio_ffmpeg
from pathlib import Path
from typing import Tuple, List, Optional
import edge_tts
from app.config import settings

logger = logging.getLogger("viralloop.assets")

def get_ffmpeg_exe() -> str:
    path = shutil.which("ffmpeg")
    if path:
        return path
    try:
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"

def clean_text_for_speech(text: str) -> str:
    """Cleans smart quotes, dashes, and unicode symbols for flawless TTS synthesis."""
    text = unicodedata.normalize('NFKD', text)
    replacements = {
        '—': ' - ',
        '–': ' - ',
        '“': '"',
        '”': '"',
        '‘': "'",
        '’': "'",
        '…': '...',
        '•': '',
        '#': 'hashtag ',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.strip()

class AssetManagerService:
    def __init__(self):
        self.ffmpeg_exe = get_ffmpeg_exe()

    async def generate_voiceover_and_subtitles(
        self, script_text: str, base_id: str
    ) -> Tuple[Path, Path, float]:
        """
        Synthesizes script into neural voiceover MP3 using Edge-TTS
        with automatic pyttsx3 offline fallback and generates synchronized subtitles.
        """
        audio_path = settings.AUDIO_DIR / f"{base_id}.mp3"
        subtitle_path = settings.SUBTITLES_DIR / f"{base_id}.srt"
        cleaned_text = clean_text_for_speech(script_text)

        # Attempt 1: Edge-TTS Microsoft Neural Voice
        try:
            logger.info(f"Synthesizing neural voiceover via Edge-TTS ({settings.TTS_VOICE})...")
            communicate = edge_tts.Communicate(
                cleaned_text,
                voice=settings.TTS_VOICE,
                rate=settings.TTS_RATE
            )
            
            submaker = edge_tts.SubMaker()
            audio_data = bytearray()

            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data.extend(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    submaker.feed(chunk)

            if len(audio_data) > 1000:
                with open(audio_path, "wb") as f:
                    f.write(audio_data)
                raw_srt = submaker.get_srt()
            else:
                raise ValueError("Edge-TTS produced empty audio stream")

        except Exception as e:
            logger.warning(f"Edge-TTS neural synthesis failed ({e}). Falling back to local TTS engine...")
            raw_srt = ""
            await self._synthesize_local_tts(cleaned_text, audio_path)

        # Measure audio duration
        duration = await self.get_media_duration(audio_path)

        # Ensure valid formatted subtitles
        if not raw_srt or len(raw_srt.strip()) < 10:
            raw_srt = self._synthesize_timed_subtitles(cleaned_text, duration)

        with open(subtitle_path, "w", encoding="utf-8") as f:
            f.write(raw_srt)

        logger.info(f"Voiceover successfully generated ({duration:.1f}s) -> {audio_path.name}")
        return audio_path, subtitle_path, duration

    async def _synthesize_local_tts(self, text: str, output_path: Path):
        """Offline fallback voice synthesizer using Windows SAPI5 via pyttsx3."""
        def _speak():
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 185)  # Punchy shorts tempo
            engine.save_to_file(text, str(output_path))
            engine.runAndWait()
        
        await asyncio.to_thread(_speak)

    def _synthesize_timed_subtitles(self, text: str, total_duration: float) -> str:
        """Splits words into 3-word punchy Shorts captions with even timing."""
        words = text.split()
        if not words:
            return ""
        
        chunk_size = 3
        chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
        chunk_duration = total_duration / max(len(chunks), 1)

        srt_lines = []
        for i, chunk in enumerate(chunks):
            start_s = i * chunk_duration
            end_s = min((i + 1) * chunk_duration, total_duration)
            
            start_tc = self._format_timestamp(start_s)
            end_tc = self._format_timestamp(end_s)
            phrase = " ".join(chunk).upper()

            srt_lines.append(f"{i + 1}\n{start_tc} --> {end_tc}\n{phrase}\n")

        return "\n".join(srt_lines)

    def _format_timestamp(self, seconds: float) -> str:
        millis = int((seconds - int(seconds)) * 1000)
        mins, secs = divmod(int(seconds), 60)
        hrs, mins = divmod(mins, 60)
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

    async def get_media_duration(self, media_path: Path) -> float:
        """Gets exact media duration in seconds via FFmpeg."""
        try:
            cmd = [
                self.ffmpeg_exe,
                "-i", str(media_path),
                "-hide_banner"
            ]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            _, stderr = await process.communicate()
            err_text = stderr.decode(errors="ignore")

            for line in err_text.splitlines():
                if "Duration:" in line:
                    time_part = line.split("Duration:")[1].split(",")[0].strip()
                    parts = time_part.split(":")
                    if len(parts) == 3:
                        h, m, s = float(parts[0]), float(parts[1]), float(parts[2])
                        return h * 3600 + m * 60 + s
        except Exception as e:
            logger.warning(f"Error reading media duration: {e}")
        return 20.0

    async def ensure_vertical_background(self, duration: float, keywords: List[str], base_id: str) -> Path:
        """
        Creates a guaranteed 1080x1920 30fps vertical video background loop.
        """
        target_clip = settings.ASSETS_DIR / f"bg_{base_id}.mp4"

        # Check if existing custom clip is present
        custom_assets = [
            f for f in settings.ASSETS_DIR.glob("*.mp4")
            if not f.name.startswith("bg_")
        ]
        if custom_assets:
            return custom_assets[0]

        # Robust testsrc2 visual pattern with vibrant saturation and dark contrast
        filter_str = (
            "testsrc2=size=1080x1920:rate=30,"
            "hue=H=2*PI*t/10:s=2.2,"
            "boxblur=luma_radius=16:luma_power=2,"
            "eq=contrast=1.35:brightness=-0.12:saturation=1.9"
        )

        render_duration = max(int(duration) + 3, 5)
        cmd = [
            self.ffmpeg_exe,
            "-y",
            "-f", "lavfi",
            "-i", filter_str,
            "-t", str(render_duration),
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-pix_fmt", "yuv420p",
            str(target_clip.resolve())
        ]

        logger.info(f"Rendering 9:16 background loop ({render_duration}s)...")
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()
        return target_clip

    async def generate_thumbnail(self, video_path: Path, output_thumb: Path, title: str) -> Path:
        """Extracts frame for video thumbnail."""
        try:
            cmd = [
                self.ffmpeg_exe,
                "-y",
                "-ss", "00:00:01.000",
                "-i", str(video_path),
                "-vframes", "1",
                "-q:v", "2",
                str(output_thumb)
            ]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
        except Exception as e:
            logger.warning(f"Error creating thumbnail: {e}")
        return output_thumb

asset_manager = AssetManagerService()
