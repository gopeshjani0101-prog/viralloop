from fastapi import APIRouter
from app.db import get_all_videos
from app.services.analytics_collector import analytics_collector

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/overview")
async def get_overview():
    videos = await get_all_videos()
    total_videos = len(videos)
    total_views = sum(v.get("views", 0) for v in videos)
    total_likes = sum(v.get("likes", 0) for v in videos)
    total_comments = sum(v.get("comments", 0) for v in videos)
    avg_retention = (
        round(sum(v.get("retention_rate", 0.0) for v in videos) / total_videos, 1)
        if total_videos > 0 else 0.0
    )

    # Calculate engagement rate
    engagement_rate = (
        round(((total_likes + total_comments) / max(total_views, 1)) * 100, 2)
        if total_views > 0 else 0.0
    )

    # Top performing video
    top_video = max(videos, key=lambda x: x.get("views", 0), default=None)

    # Generate timeline points for charts
    timeline = []
    for v in reversed(videos[:10]):
        timeline.append({
            "title": v.get("title", "")[:20] + "...",
            "views": v.get("views", 0),
            "retention": v.get("retention_rate", 0.0),
            "likes": v.get("likes", 0),
            "created_at": v.get("created_at", "")
        })

    return {
        "total_videos": total_videos,
        "total_views": total_views,
        "total_likes": total_likes,
        "total_comments": total_comments,
        "avg_retention": avg_retention,
        "engagement_rate": engagement_rate,
        "top_video": top_video,
        "timeline": timeline
    }

@router.post("/refresh")
async def refresh_metrics():
    updated = await analytics_collector.refresh_all_metrics()
    return {"message": "Metrics refreshed", "updated_count": len(updated)}
