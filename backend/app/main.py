import logging
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.db import init_db
from app.routes.pipeline import router as pipeline_router
from app.routes.videos import router as videos_router
from app.routes.analytics import router as analytics_router
from app.routes.learning import router as learning_router
from app.routes.settings import router as settings_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("viralloop.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing ViralLoop SQLite database...")
    await init_db()
    logger.info("ViralLoop backend ready!")
    yield
    logger.info("Shutting down ViralLoop backend...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(pipeline_router)
app.include_router(videos_router)
app.include_router(analytics_router)
app.include_router(learning_router)
app.include_router(settings_router)

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "sqlite_ready",
        "ollama_target": settings.OLLAMA_MODEL,
        "youtube_mode": settings.YOUTUBE_MODE
    }

# Mount Frontend Dist if available
FRONTEND_DIST = settings.STORAGE_DIR.parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists() and (FRONTEND_DIST / "index.html").exists():
    logger.info(f"Mounting built React frontend from {FRONTEND_DIST}")
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="frontend")
else:
    @app.get("/")
    async def root():
        return {
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "online",
            "docs_url": "/docs"
        }
