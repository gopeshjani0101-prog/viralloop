import aiosqlite
import json
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from app.config import settings

async def get_db():
    async with aiosqlite.connect(settings.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        yield db

async def init_db():
    """Initializes tables and seeds starting viral rules if empty."""
    async with aiosqlite.connect(settings.DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                hook TEXT NOT NULL,
                script TEXT NOT NULL,
                tags TEXT NOT NULL,
                category TEXT DEFAULT 'Technology',
                duration REAL DEFAULT 0.0,
                video_url TEXT DEFAULT '',
                file_path TEXT DEFAULT '',
                audio_path TEXT DEFAULT '',
                subtitle_path TEXT DEFAULT '',
                thumbnail_url TEXT DEFAULT '',
                youtube_id TEXT DEFAULT '',
                youtube_url TEXT DEFAULT '',
                youtube_status TEXT DEFAULT 'published',
                views INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                retention_rate REAL DEFAULT 0.0,
                shares INTEGER DEFAULT 0,
                virality_score INTEGER DEFAULT 85,
                actual_score REAL DEFAULT 0.0,
                prompt_iteration INTEGER DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS pipeline_runs (
                id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                current_step TEXT NOT NULL,
                progress INTEGER DEFAULT 0,
                topic TEXT DEFAULT '',
                video_id TEXT,
                logs TEXT DEFAULT '[]',
                error TEXT,
                created_at TEXT NOT NULL,
                completed_at TEXT
            );
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS learning_insights (
                id TEXT PRIMARY KEY,
                iteration INTEGER NOT NULL,
                rule_name TEXT NOT NULL,
                rule_description TEXT NOT NULL,
                impact TEXT NOT NULL,
                metric_improvement TEXT NOT NULL,
                applied_prompt_snippet TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
        """)

        # Check if learning_insights has seed rules
        async with db.execute("SELECT COUNT(*) as count FROM learning_insights") as cursor:
            row = await cursor.fetchone()
            if row and row[0] == 0:
                seed_insights = [
                    (
                        str(uuid.uuid4()),
                        1,
                        "Curiosity Gap Hook",
                        "Begin within first 2 seconds with an unanswered provocative question or counter-intuitive claim.",
                        "high_positive",
                        "+38% Retention in 0-5s window",
                        "Rule: Never say 'Hey guys' or introduce yourself. State the mystery immediately.",
                        datetime.now().isoformat()
                    ),
                    (
                        str(uuid.uuid4()),
                        1,
                        "Hyper-Paced Micro-Sentences",
                        "Keep sentences under 8 words each so TTS pacing remains rapid and subtitles flash rhythmically.",
                        "positive",
                        "+24% Completion rate",
                        "Rule: Split compound sentences into punchy declarations.",
                        datetime.now().isoformat()
                    ),
                    (
                        str(uuid.uuid4()),
                        1,
                        "Looping Ending Pattern",
                        "Craft the final sentence to naturally flow right back into the video's opening hook line.",
                        "high_positive",
                        "+42% Loop replay rate on Shorts feed",
                        "Rule: End video with seamless transition connecting to the first hook word.",
                        datetime.now().isoformat()
                    )
                ]
                await db.executemany(
                    """
                    INSERT INTO learning_insights (id, iteration, rule_name, rule_description, impact, metric_improvement, applied_prompt_snippet, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    seed_insights
                )

        await db.commit()

# --- Video DB Helpers ---

async def save_video(video_data: Dict[str, Any]) -> str:
    async with aiosqlite.connect(settings.DB_PATH) as db:
        now = datetime.now().isoformat()
        tags_str = json.dumps(video_data.get("tags", []))
        video_id = video_data.get("id") or str(uuid.uuid4())
        
        await db.execute(
            """
            INSERT OR REPLACE INTO videos (
                id, title, hook, script, tags, category, duration, video_url,
                file_path, audio_path, subtitle_path, thumbnail_url, youtube_id,
                youtube_url, youtube_status, views, likes, comments, retention_rate,
                shares, virality_score, actual_score, prompt_iteration, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                video_id,
                video_data.get("title", "Untitled Short"),
                video_data.get("hook", ""),
                video_data.get("script", ""),
                tags_str,
                video_data.get("category", "Technology"),
                video_data.get("duration", 0.0),
                video_data.get("video_url", ""),
                video_data.get("file_path", ""),
                video_data.get("audio_path", ""),
                video_data.get("subtitle_path", ""),
                video_data.get("thumbnail_url", ""),
                video_data.get("youtube_id", ""),
                video_data.get("youtube_url", ""),
                video_data.get("youtube_status", "published"),
                video_data.get("views", 0),
                video_data.get("likes", 0),
                video_data.get("comments", 0),
                video_data.get("retention_rate", 0.0),
                video_data.get("shares", 0),
                video_data.get("virality_score", 85),
                video_data.get("actual_score", 0.0),
                video_data.get("prompt_iteration", 1),
                video_data.get("created_at", now),
                now
            )
        )
        await db.commit()
        return video_id

async def get_all_videos() -> List[Dict[str, Any]]:
    async with aiosqlite.connect(settings.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM videos ORDER BY created_at DESC") as cursor:
            rows = await cursor.fetchall()
            results = []
            for row in rows:
                item = dict(row)
                try:
                    item["tags"] = json.loads(item["tags"])
                except Exception:
                    item["tags"] = []
                results.append(item)
            return results

async def get_video_by_id(video_id: str) -> Optional[Dict[str, Any]]:
    async with aiosqlite.connect(settings.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM videos WHERE id = ?", (video_id,)) as cursor:
            row = await cursor.fetchone()
            if not row:
                return None
            item = dict(row)
            try:
                item["tags"] = json.loads(item["tags"])
            except Exception:
                item["tags"] = []
            return item

async def update_video_metrics(video_id: str, metrics: Dict[str, Any]):
    async with aiosqlite.connect(settings.DB_PATH) as db:
        await db.execute(
            """
            UPDATE videos
            SET views = ?, likes = ?, comments = ?, retention_rate = ?, shares = ?, actual_score = ?, updated_at = ?
            WHERE id = ?
            """,
            (
                metrics.get("views", 0),
                metrics.get("likes", 0),
                metrics.get("comments", 0),
                metrics.get("retention_rate", 0.0),
                metrics.get("shares", 0),
                metrics.get("actual_score", 0.0),
                datetime.now().isoformat(),
                video_id
            )
        )
        await db.commit()

# --- Pipeline Run Helpers ---

async def create_pipeline_run(run_id: str, topic: str = "") -> Dict[str, Any]:
    async with aiosqlite.connect(settings.DB_PATH) as db:
        now = datetime.now().isoformat()
        logs = [{"time": now, "step": "init", "message": "Pipeline initiated"}]
        await db.execute(
            """
            INSERT INTO pipeline_runs (id, status, current_step, progress, topic, logs, created_at)
            VALUES (?, 'starting', 'Discovery', 5, ?, ?, ?)
            """,
            (run_id, topic, json.dumps(logs), now)
        )
        await db.commit()
        return {"id": run_id, "status": "starting", "current_step": "Discovery", "progress": 5}

async def update_pipeline_run(run_id: str, step: str, progress: int, status: str = "running", message: str = "", video_id: Optional[str] = None, error: Optional[str] = None):
    async with aiosqlite.connect(settings.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT logs FROM pipeline_runs WHERE id = ?", (run_id,)) as cursor:
            row = await cursor.fetchone()
            logs = []
            if row and row["logs"]:
                try:
                    logs = json.loads(row["logs"])
                except Exception:
                    logs = []

        now = datetime.now().isoformat()
        if message:
            logs.append({"time": now, "step": step, "message": message})

        completed_at = now if status in ["completed", "failed"] else None

        await db.execute(
            """
            UPDATE pipeline_runs
            SET status = ?, current_step = ?, progress = ?, logs = ?, video_id = COALESCE(?, video_id), error = ?, completed_at = COALESCE(?, completed_at)
            WHERE id = ?
            """,
            (status, step, progress, json.dumps(logs), video_id, error, completed_at, run_id)
        )
        await db.commit()

async def get_latest_pipeline_run() -> Optional[Dict[str, Any]]:
    async with aiosqlite.connect(settings.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM pipeline_runs ORDER BY created_at DESC LIMIT 1") as cursor:
            row = await cursor.fetchone()
            if not row:
                return None
            item = dict(row)
            try:
                item["logs"] = json.loads(item["logs"])
            except Exception:
                item["logs"] = []
            return item

# --- Learning Insights Helpers ---

async def get_all_insights() -> List[Dict[str, Any]]:
    async with aiosqlite.connect(settings.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM learning_insights ORDER BY created_at DESC") as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

async def add_learning_insight(rule_name: str, rule_desc: str, impact: str, improvement: str, snippet: str, iteration: int = 1):
    async with aiosqlite.connect(settings.DB_PATH) as db:
        insight_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        await db.execute(
            """
            INSERT INTO learning_insights (id, iteration, rule_name, rule_description, impact, metric_improvement, applied_prompt_snippet, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (insight_id, iteration, rule_name, rule_desc, impact, improvement, snippet, now)
        )
        await db.commit()
        return insight_id
