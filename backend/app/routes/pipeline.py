from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.pipeline_orchestrator import pipeline_orchestrator
from app.db import get_latest_pipeline_run

router = APIRouter(prefix="/api/pipeline", tags=["Pipeline"])

class TriggerPipelineRequest(BaseModel):
    topic: Optional[str] = None

class AutonomousSettingsRequest(BaseModel):
    interval_seconds: int = 120

@router.post("/run")
async def trigger_run(req: TriggerPipelineRequest, background_tasks: BackgroundTasks):
    """Triggers one complete autonomous loop in background."""
    if pipeline_orchestrator.is_running:
        raise HTTPException(status_code=400, detail="A pipeline loop is currently in progress.")
    
    background_tasks.add_task(pipeline_orchestrator.run_single_loop, req.topic)
    return {"message": "Pipeline cycle initiated", "topic": req.topic or "Auto-discovered"}

@router.get("/status")
async def get_status():
    """Returns current active step, logs, and progress of the pipeline."""
    latest_run = await get_latest_pipeline_run()
    return {
        "is_running": pipeline_orchestrator.is_running,
        "autonomous_mode": pipeline_orchestrator.autonomous_mode,
        "current_run": latest_run
    }

@router.post("/autonomous/start")
async def start_autonomous(req: AutonomousSettingsRequest = AutonomousSettingsRequest()):
    pipeline_orchestrator.start_autonomous_loop(req.interval_seconds)
    return {"status": "started", "interval_seconds": req.interval_seconds}

@router.post("/autonomous/stop")
async def stop_autonomous():
    pipeline_orchestrator.stop_autonomous_loop()
    return {"status": "stopped"}

@router.get("/autonomous/status")
async def autonomous_status():
    return {
        "autonomous_mode": pipeline_orchestrator.autonomous_mode,
        "is_running": pipeline_orchestrator.is_running
    }
