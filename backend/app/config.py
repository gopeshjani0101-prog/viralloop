import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent
STORAGE_DIR = BACKEND_DIR / "storage"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "ViralLoop"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Database
    DB_PATH: str = str(BACKEND_DIR / "viralloop.db")

    # Ollama Local LLM
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "gemma4"  # Also supports gemma:2b, qwen2.5:3b, etc.
    OLLAMA_TIMEOUT: float = 90.0

    # YouTube Mode
    YOUTUBE_MODE: str = "simulated"  # "simulated" or "live"
    YOUTUBE_CLIENT_SECRETS_FILE: str = str(BACKEND_DIR / "client_secrets.json")
    YOUTUBE_TOKEN_FILE: str = str(BACKEND_DIR / "token.json")

    # Text to Speech
    TTS_VOICE: str = "en-US-ChristopherNeural"
    TTS_RATE: str = "+15%"  # Paced for short vertical videos

    # Storage Dirs
    STORAGE_DIR: Path = STORAGE_DIR
    VIDEOS_DIR: Path = STORAGE_DIR / "videos"
    AUDIO_DIR: Path = STORAGE_DIR / "audio"
    ASSETS_DIR: Path = STORAGE_DIR / "assets"
    SUBTITLES_DIR: Path = STORAGE_DIR / "subtitles"

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:8000",
    ]

settings = Settings()

# Ensure storage directories exist
for path in [
    settings.STORAGE_DIR,
    settings.VIDEOS_DIR,
    settings.AUDIO_DIR,
    settings.ASSETS_DIR,
    settings.SUBTITLES_DIR,
]:
    path.mkdir(parents=True, exist_ok=True)
