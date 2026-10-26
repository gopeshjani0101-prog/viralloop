from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from app.config import settings
from app.db import get_all_videos, get_video_by_id

router = APIRouter(prefix="/api/videos", tags=["Videos"])

@router.get("")
async def list_videos():
    """Lists all produced videos with metrics and metadata."""
    videos = await get_all_videos()
    return {"videos": videos, "total": len(videos)}

@router.get("/{video_id}")
async def get_video(video_id: str):
    video = await get_video_by_id(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

@router.get("/stream/{filename}")
async def stream_video(filename: str):
    file_path = settings.VIDEOS_DIR / filename
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Video file not found")
    return FileResponse(path=file_path, media_type="video/mp4", filename=filename)

@router.get("/thumbnail/{filename}")
async def get_thumbnail(filename: str):
    file_path = settings.VIDEOS_DIR / filename
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Thumbnail not found")
    return FileResponse(path=file_path, media_type="image/jpeg", filename=filename)
