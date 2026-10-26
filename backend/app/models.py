from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class VideoModel(BaseModel):
    id: str
    title: str
    hook: str
    script: str
    tags: List[str] = Field(default_factory=list)
    category: str = "Technology & Science"
    duration: float = 0.0
    video_url: str = ""
    file_path: str = ""
    audio_path: str = ""
    subtitle_path: str = ""
    thumbnail_url: str = ""
    youtube_id: str = ""
    youtube_url: str = ""
    youtube_status: str = "published"
    views: int = 0
    likes: int = 0
    comments: int = 0
    retention_rate: float = 0.0
    shares: int = 0
    virality_score: int = 85
    actual_score: float = 0.0
    prompt_iteration: int = 1
    created_at: str
    updated_at: str

class PipelineRunModel(BaseModel):
    id: str
    status: str
    current_step: str
    progress: int = 0
    topic: str = ""
    video_id: Optional[str] = None
    logs: List[Dict[str, Any]] = Field(default_factory=list)
    error: Optional[str] = None
    created_at: str
    completed_at: Optional[str] = None

class LearningInsightModel(BaseModel):
    id: str
    iteration: int
    rule_name: str
    rule_description: str
    impact: str
    metric_improvement: str
    applied_prompt_snippet: str
    created_at: str

class TrendingTopic(BaseModel):
    source: str
    title: str
    url: str
    score: int
    num_comments: int
    summary: str = ""

class ScriptGenerationResult(BaseModel):
    selected_topic: str
    topic_summary: str
    virality_score: int
    virality_rationale: str
    title: str
    hook: str
    script: str
    tags: List[str]
    target_audience: str
    visual_keywords: List[str]
