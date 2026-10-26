from fastapi import APIRouter
from app.db import get_all_insights

router = APIRouter(prefix="/api/learning", tags=["Learning"])

@router.get("/insights")
async def list_insights():
    """Returns all learned viral rules and evolution history."""
    insights = await get_all_insights()
    return {
        "insights": insights,
        "total_rules": len(insights)
    }
