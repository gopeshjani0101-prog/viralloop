import os
import asyncio
import logging
from pathlib import Path
from typing import Tuple
from app.config import settings
from app.services.asset_manager import get_ffmpeg_exe, asset_manager

logger = logging.getLogger("viralloop.editor")

class VideoEditorService:
    def __init__(self):
        self.ffmpeg_exe = get_ffmpeg_exe()

    async def render_short_video(
        self,
        base_id: str,
        background_video: Path,
        audio_file: Path,
        subtitle_file: Path,
        duration: float,
        title: str
    ) -> Tuple[Path, Path]:
        """
        Renders complete 9:16 vertical video with:
        - 1080x1920 vertical format
        - Standard 44.1kHz stereo AAC audio normalization for universal web playback
        - Burned-in high-contrast subtitles
        - Faststart metadata for instant streaming
        """
        output_video_path = settings.VIDEOS_DIR / f"{base_id}.mp4"
        output_thumb_path = settings.VIDEOS_DIR / f"{base_id}_thumb.jpg"

        work_sub = subtitle_file.resolve()
        sub_filter_path = work_sub.name
        cwd_dir = subtitle_file.parent

        style_args = (
            "FontSize=26,"
            "PrimaryColour=&H0000FFFF,"
            "OutlineColour=&H00000000,"
            "BackColour=&H80000000,"
            "Bold=1,"
            "BorderStyle=3,"
            "Outline=3,"
            "Shadow=1,"
            "Alignment=2,"
            "MarginV=380"
        )
        style_escaped = style_args.replace(",", "\\,")
        sub_filter = f"subtitles={sub_filter_path}:force_style={style_escaped}"

        # Combine video, audio (44.1kHz stereo AAC), and subtitle burn-in
        cmd = [
            self.ffmpeg_exe,
            "-y",
            "-stream_loop", "-1",
            "-i", str(background_video.resolve()),
            "-i", str(audio_file.resolve()),
            "-vf", sub_filter,
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "22",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "44100",
            "-ac", "2",
            "-t", f"{duration + 0.3:.2f}",
            "-movflags", "+faststart",
            str(output_video_path.resolve())
        ]

        logger.info(f"Rendering final Short MP4 ({duration:.1f}s) to {output_video_path.name}...")
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=str(cwd_dir),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            err_msg = stderr.decode(errors="ignore")
            logger.error(f"FFmpeg render error: {err_msg}")
            # Fallback without subtitle filter
            fallback_cmd = [
                self.ffmpeg_exe,
                "-y",
                "-stream_loop", "-1",
                "-i", str(background_video.resolve()),
                "-i", str(audio_file.resolve()),
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-c:a", "aac",
                "-b:a", "192k",
                "-ar", "44100",
                "-ac", "2",
                "-t", f"{duration + 0.3:.2f}",
                "-movflags", "+faststart",
                str(output_video_path.resolve())
            ]
            fb_proc = await asyncio.create_subprocess_exec(*fallback_cmd)
            await fb_proc.communicate()

        # Generate thumbnail
        await asset_manager.generate_thumbnail(output_video_path, output_thumb_path, title)

        return output_video_path, output_thumb_path

video_editor = VideoEditorService()
