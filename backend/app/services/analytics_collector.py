import random
import logging
from typing import Dict, Any, List
from app.db import get_all_videos, update_video_metrics

logger = logging.getLogger("viralloop.analytics")

class AnalyticsCollectorService:
    async def refresh_all_metrics(self) -> List[Dict[str, Any]]:
        """Simulates or scrapes real-time metrics for all posted videos."""
        videos = await get_all_videos()
        updated = []

        for v in videos:
            vid = v["id"]
            curr_views = v.get("views", 100)
            curr_likes = v.get("likes", 10)
            curr_comments = v.get("comments", 2)
            retention = v.get("retention_rate", 75.0)

            # Growth simulation: videos gradually accrue organic feed impressions
            growth_factor = random.uniform(1.05, 1.25) if retention > 80 else random.uniform(1.01, 1.08)
            new_views = int(curr_views * growth_factor)
            new_likes = int(curr_likes + ((new_views - curr_views) * random.uniform(0.06, 0.12)))
            new_comments = int(curr_comments + ((new_likes - curr_likes) * random.uniform(0.04, 0.08)))
            
            # Retention fluctuates slightly around baseline
            new_retention = round(max(50.0, min(98.0, retention + random.uniform(-1.5, 1.8))), 1)
            shares = int(new_likes * random.uniform(0.03, 0.06))
            actual_score = round((new_retention * 0.6) + ((new_likes / max(new_views, 1)) * 400), 1)

            metrics = {
                "views": new_views,
                "likes": new_likes,
                "comments": new_comments,
                "retention_rate": new_retention,
                "shares": shares,
                "actual_score": actual_score
            }

            await update_video_metrics(vid, metrics)
            v.update(metrics)
            updated.append(v)

        return updated

analytics_collector = AnalyticsCollectorService()
