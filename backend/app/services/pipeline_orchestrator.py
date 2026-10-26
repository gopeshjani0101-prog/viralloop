import asyncio
import uuid
import logging
from typing import Dict, Any, Optional
from app.db import (
    create_pipeline_run,
    update_pipeline_run,
    save_video,
    get_video_by_id
)
from app.services.discovery import discovery_service
from app.services.llm_reasoning import llm_service
from app.services.asset_manager import asset_manager
from app.services.video_editor import video_editor
from app.services.youtube_publisher import youtube_publisher
from app.services.learning_agent import learning_agent

logger = logging.getLogger("viralloop.pipeline")

class PipelineOrchestrator:
    def __init__(self):
        self.is_running = False
        self.autonomous_mode = False
        self._autonomous_task: Optional[asyncio.Task] = None

    async def run_single_loop(self, custom_topic: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes one full autonomous cycle:
        1. Discover Trending Ideas
        2. LLM Reasoning (Gemma 4 Hook & Script Generation)
        3. Neural Voice & Asset Assembly
        4. Vertical 9:16 Video Editing & Burned-in Subtitles
        5. YouTube Shorts Publishing
        6. Analytics & Evolutionary Learning Loop
        """
        run_id = str(uuid.uuid4())
        self.is_running = True

        try:
            await create_pipeline_run(run_id, topic=custom_topic or "Autonomous Discovery")

            # --- STEP 1: Discovery ---
            await update_pipeline_run(
                run_id,
                step="Discovery",
                progress=15,
                message="Scanning Reddit, HackerNews, and Trends for high-velocity topics..."
            )
            trending_topics = await discovery_service.discover_trending_ideas()
            if custom_topic:
                from app.models import TrendingTopic
                trending_topics.insert(0, TrendingTopic(
                    source="User Selected",
                    title=custom_topic,
                    url="https://viralloop.local",
                    score=9999,
                    num_comments=500,
                    summary=custom_topic
                ))

            # --- STEP 2: LLM Reasoning (Gemma) ---
            await update_pipeline_run(
                run_id,
                step="LLM Reasoning",
                progress=35,
                message="Gemma 4 reasoning active: scoring virality, crafting 3s hook, and structuring loop script..."
            )
            script_data = await llm_service.generate_viral_content(trending_topics)
            base_id = str(uuid.uuid4())[:8]

            # --- STEP 3: Voiceover & Assets ---
            await update_pipeline_run(
                run_id,
                step="Asset Generation",
                progress=55,
                message=f"Synthesizing neural voiceover and generating 9:16 visual assets for '{script_data.title}'..."
            )
            audio_path, subtitle_path, duration = await asset_manager.generate_voiceover_and_subtitles(
                script_data.script, base_id
            )
            bg_video_path = await asset_manager.ensure_vertical_background(
                duration, script_data.visual_keywords, base_id
            )

            # --- STEP 4: Video Editing & Subtitles ---
            await update_pipeline_run(
                run_id,
                step="Video Editing",
                progress=75,
                message="FFmpeg compositing 1080x1920 video, synchronizing audio, and burning styled captions..."
            )
            video_path, thumb_path = await video_editor.render_short_video(
                base_id, bg_video_path, audio_path, subtitle_path, duration, script_data.title
            )

            # --- STEP 5: YouTube Shorts Publishing ---
            await update_pipeline_run(
                run_id,
                step="Publishing",
                progress=88,
                message="Publishing video to YouTube Shorts with optimized SEO tags..."
            )
            pub_result = await youtube_publisher.publish_short(
                video_path=video_path,
                title=script_data.title,
                description=f"{script_data.script}\n\n{' '.join(script_data.tags)}",
                tags=script_data.tags,
                virality_score=script_data.virality_score
            )

            # Save Video Record to Database
            video_id = str(uuid.uuid4())
            metrics = pub_result.get("initial_metrics", {})
            video_record = {
                "id": video_id,
                "title": script_data.title,
                "hook": script_data.hook,
                "script": script_data.script,
                "tags": script_data.tags,
                "category": script_data.target_audience,
                "duration": duration,
                "video_url": f"/api/videos/stream/{video_path.name}",
                "file_path": str(video_path),
                "audio_path": str(audio_path),
                "subtitle_path": str(subtitle_path),
                "thumbnail_url": f"/api/videos/thumbnail/{thumb_path.name}",
                "youtube_id": pub_result.get("youtube_id", ""),
                "youtube_url": pub_result.get("youtube_url", ""),
                "youtube_status": pub_result.get("status", "published"),
                "views": metrics.get("views", 0),
                "likes": metrics.get("likes", 0),
                "comments": metrics.get("comments", 0),
                "retention_rate": metrics.get("retention_rate", 0.0),
                "shares": metrics.get("shares", 0),
                "virality_score": script_data.virality_score,
                "actual_score": metrics.get("actual_score", 0.0)
            }
            await save_video(video_record)

            # --- STEP 6: Evolutionary Learning Feedback Loop ---
            await update_pipeline_run(
                run_id,
                step="Learning Loop",
                progress=96,
                video_id=video_id,
                message="Agent analyzing viewer retention statistics to evolve next generation viral rules..."
            )
            new_heuristic = await learning_agent.analyze_and_evolve(video_record)

            # Pipeline Complete
            await update_pipeline_run(
                run_id,
                step="Completed",
                progress=100,
                status="completed",
                video_id=video_id,
                message=f"Loop complete! Learned new rule: {new_heuristic.get('rule_name')} ({new_heuristic.get('metric_improvement')})"
            )

            return {
                "run_id": run_id,
                "video_id": video_id,
                "title": script_data.title,
                "youtube_url": pub_result.get("youtube_url", ""),
                "learned_rule": new_heuristic
            }

        except Exception as e:
            logger.exception(f"Pipeline error in run {run_id}: {e}")
            await update_pipeline_run(
                run_id,
                step="Failed",
                progress=0,
                status="failed",
                error=str(e),
                message=f"Pipeline failed: {str(e)}"
            )
            raise e
        finally:
            self.is_running = False

    def start_autonomous_loop(self, interval_seconds: int = 120):
        """Starts background continuous autonomous loop."""
        if self.autonomous_mode:
            return
        self.autonomous_mode = True

        async def _loop():
            logger.info("Autonomous Viral Loop started!")
            while self.autonomous_mode:
                try:
                    logger.info("Autonomous cycle starting...")
                    await self.run_single_loop()
                except Exception as e:
                    logger.error(f"Error in autonomous loop cycle: {e}")
                
                # Sleep interval before next autonomous loop
                for _ in range(interval_seconds):
                    if not self.autonomous_mode:
                        break
                    await asyncio.sleep(1)

        self._autonomous_task = asyncio.create_task(_loop())

    def stop_autonomous_loop(self):
        """Stops background continuous autonomous loop."""
        self.autonomous_mode = False
        if self._autonomous_task:
            self._autonomous_task.cancel()
            self._autonomous_task = None
        logger.info("Autonomous Viral Loop stopped.")

pipeline_orchestrator = PipelineOrchestrator()
