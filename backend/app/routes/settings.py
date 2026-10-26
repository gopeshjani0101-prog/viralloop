from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from app.config import settings
from app.services.llm_reasoning import llm_service

router = APIRouter(prefix="/api/settings", tags=["Settings"])

class UpdateSettingsRequest(BaseModel):
    ollama_model: Optional[str] = None
    youtube_mode: Optional[str] = None
    tts_voice: Optional[str] = None

@router.get("")
async def get_settings():
    available_models = await llm_service.get_available_models()
    active_model = await llm_service.select_best_model()

    return {
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION,
        "ollama_base_url": settings.OLLAMA_BASE_URL,
        "ollama_configured_model": settings.OLLAMA_MODEL,
        "ollama_active_model": active_model,
        "available_models": available_models,
        "youtube_mode": settings.YOUTUBE_MODE,
        "tts_voice": settings.TTS_VOICE,
        "tts_rate": settings.TTS_RATE
    }

@router.post("")
async def update_settings(req: UpdateSettingsRequest):
    if req.ollama_model:
        settings.OLLAMA_MODEL = req.ollama_model
        llm_service.default_model = req.ollama_model
    if req.youtube_mode:
        settings.YOUTUBE_MODE = req.youtube_mode
    if req.tts_voice:
        settings.TTS_VOICE = req.tts_voice
    
    return {"message": "Settings updated successfully", "current_model": settings.OLLAMA_MODEL}
