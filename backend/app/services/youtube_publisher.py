import os
import random
import string
import logging
from pathlib import Path
from typing import Dict, Any, List
from app.config import settings

logger = logging.getLogger("viralloop.publisher")

class YouTubePublisherService:
    def __init__(self):
        self.mode = settings.YOUTUBE_MODE

    def _generate_mock_id(self) -> str:
        chars = string.ascii_letters + string.digits + "_-"
        return "".join(random.choice(chars) for _ in range(11))

    async def publish_short(
        self,
        video_path: Path,
        title: str,
        description: str,
        tags: List[str],
        virality_score: int
    ) -> Dict[str, Any]:
        """
        Publishes video to YouTube Shorts.
        If live credentials exist and mode is 'live', uses YouTube Data API v3.
        Otherwise executes high-fidelity simulator mode for hackathon demos.
        """
        client_secrets_path = Path(settings.YOUTUBE_CLIENT_SECRETS_FILE)

        # Check if live upload can be performed
        if self.mode == "live" and client_secrets_path.exists():
            try:
                return await self._live_upload(video_path, title, description, tags)
            except Exception as e:
                logger.warning(f"Live YouTube upload failed ({e}), falling back to simulator.")

        return self._simulated_upload(video_path, title, description, tags, virality_score)

    def _simulated_upload(
        self,
        video_path: Path,
        title: str,
        description: str,
        tags: List[str],
        virality_score: int
    ) -> Dict[str, Any]:
        """Generates realistic YouTube Shorts publishing event with simulated metrics."""
        youtube_id = self._generate_mock_id()
        youtube_url = f"https://www.youtube.com/shorts/{youtube_id}"

        # Initial launch views influenced by virality score
        base_views = int(random.randint(450, 1800) * (virality_score / 75.0))
        likes = int(base_views * random.uniform(0.06, 0.12))
        comments = int(likes * random.uniform(0.04, 0.10))
        retention = round(random.uniform(68.0, 94.0), 1)
        shares = int(likes * random.uniform(0.02, 0.05))

        logger.info(f"[SIMULATED YOUTUBE] Video published! URL: {youtube_url}")

        return {
            "mode": "simulated",
            "youtube_id": youtube_id,
            "youtube_url": youtube_url,
            "status": "published",
            "privacy": "public",
            "initial_metrics": {
                "views": base_views,
                "likes": likes,
                "comments": comments,
                "retention_rate": retention,
                "shares": shares,
                "actual_score": round((retention * 0.5) + ((likes / max(base_views, 1)) * 500), 1)
            }
        }

    async def _live_upload(
        self,
        video_path: Path,
        title: str,
        description: str,
        tags: List[str]
    ) -> Dict[str, Any]:
        """Live YouTube Data API v3 upload implementation."""
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from google.oauth2.credentials import Credentials

        token_path = Path(settings.YOUTUBE_TOKEN_FILE)
        if not token_path.exists():
            raise FileNotFoundError("YouTube token.json not found. Please authenticate via OAuth flow.")

        creds = Credentials.from_authorized_user_file(str(token_path))
        youtube = build("youtube", "v3", credentials=creds)

        # Ensure #Shorts is in title/description for algorithm classification
        if "#shorts" not in title.lower():
            title = f"{title} #shorts"

        body = {
            "snippet": {
                "title": title[:100],
                "description": description,
                "tags": tags,
                "categoryId": "28"  # Science & Technology
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        }

        media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True)
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        response = request.execute()

        video_id = response.get("id")
        return {
            "mode": "live",
            "youtube_id": video_id,
            "youtube_url": f"https://www.youtube.com/shorts/{video_id}",
            "status": "published",
            "privacy": "public",
            "initial_metrics": {
                "views": 0,
                "likes": 0,
                "comments": 0,
                "retention_rate": 0.0,
                "shares": 0,
                "actual_score": 0.0
            }
        }

youtube_publisher = YouTubePublisherService()
