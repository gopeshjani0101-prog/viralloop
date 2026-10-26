import httpx
import json
import logging
from typing import Dict, Any, Optional
from app.config import settings
from app.db import get_all_videos, add_learning_insight, get_all_insights
from app.services.llm_reasoning import llm_service

logger = logging.getLogger("viralloop.learning")

LEARNING_PROMPT_TEMPLATE = """You are ViralLoop's Evolutionary Reinforcement Learning Agent.
Your mission is to analyze the performance of our latest YouTube Short and channel history, extract the critical lesson, and formulate an updated guideline for the next video.

LATEST VIDEO STATS:
- Title: {title}
- Hook: {hook}
- Views: {views}
- Likes: {likes}
- Comments: {comments}
- Retention Rate: {retention_rate}%
- Virality Score (Predicted): {virality_score}
- Actual Score: {actual_score}

CHANNEL BENCHMARKS:
- Total Videos Produced: {total_videos}
- Channel Avg Retention: {avg_retention:.1f}%
- Channel Avg Views: {avg_views:.0f}

FORMULATE 1 ACTIONABLE LESSON TO IMPROVE THE NEXT VIDEO.
Respond ONLY with a JSON object in this exact schema:
{{
  "rule_name": "Short 3-5 word rule name (e.g., 'Numbers in Opening Hook')",
  "rule_description": "Precise explanation of what to do differently in the script or pacing.",
  "impact": "high_positive",
  "metric_improvement": "Projected or observed improvement (e.g., '+18% Average Watch Duration')",
  "applied_prompt_snippet": "Exact instruction text to be injected into future system prompts."
}}
"""

class LearningAgentService:
    async def analyze_and_evolve(self, latest_video_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Reflects on latest video performance vs channel historical data
        and uses Ollama (Gemma) to synthesize a new viral heuristic.
        """
        all_videos = await get_all_videos()
        total_videos = len(all_videos)
        
        if total_videos > 0:
            avg_retention = sum(v.get("retention_rate", 70.0) for v in all_videos) / total_videos
            avg_views = sum(v.get("views", 0) for v in all_videos) / total_videos
        else:
            avg_retention = 75.0
            avg_views = 1200.0

        model = await llm_service.select_best_model()

        prompt = LEARNING_PROMPT_TEMPLATE.format(
            title=latest_video_data.get("title", ""),
            hook=latest_video_data.get("hook", ""),
            views=latest_video_data.get("views", 0),
            likes=latest_video_data.get("likes", 0),
            comments=latest_video_data.get("comments", 0),
            retention_rate=latest_video_data.get("retention_rate", 0.0),
            virality_score=latest_video_data.get("virality_score", 85),
            actual_score=latest_video_data.get("actual_score", 0.0),
            total_videos=total_videos,
            avg_retention=avg_retention,
            avg_views=avg_views
        )

        try:
            async with httpx.AsyncClient(timeout=45.0) as client:
                logger.info("Triggering Ollama evolutionary analysis...")
                resp = await client.post(
                    f"{settings.OLLAMA_BASE_URL}/api/generate",
                    json={"model": model, "prompt": prompt, "stream": False}
                )
                if resp.status_code == 200:
                    raw_text = resp.json().get("response", "")
                    parsed = llm_service._extract_json(raw_text)
                    if parsed and "rule_name" in parsed and "rule_description" in parsed:
                        iteration = total_videos + 1
                        await add_learning_insight(
                            rule_name=parsed["rule_name"],
                            rule_desc=parsed["rule_description"],
                            impact=parsed.get("impact", "positive"),
                            improvement=parsed.get("metric_improvement", "+15% Engagement"),
                            snippet=parsed.get("applied_prompt_snippet", parsed["rule_description"]),
                            iteration=iteration
                        )
                        logger.info(f"Learned new viral rule: {parsed['rule_name']}")
                        return parsed
        except Exception as e:
            logger.warning(f"Ollama learning reflection error: {e}. Utilizing algorithmic synthesizer.")

        # Algorithmic fallback rule synthesizer
        retention = latest_video_data.get("retention_rate", 75.0)
        iteration = total_videos + 1

        if retention > 82.0:
            rule_name = "High-Cadence Pacing Anchor"
            rule_desc = "Fast narrative delivery paired with high contrast hook retained >82% of viewers. Double down on swift sentence cuts."
            impact = "high_positive"
            improvement = "+22% Completion Rate"
            snippet = "Rule: Maintain sentence length under 7 words for narrative peaks."
        else:
            rule_name = "Urgency Escalation Hook"
            rule_desc = "Introduce immediate consequence or tangible stake within the first 1.8 seconds to prevent feed swipe-aways."
            impact = "positive"
            improvement = "+16% Retention in 0-3s window"
            snippet = "Rule: First sentence must directly challenge or surprise the viewer's belief."

        await add_learning_insight(
            rule_name=rule_name,
            rule_desc=rule_desc,
            impact=impact,
            improvement=improvement,
            snippet=snippet,
            iteration=iteration
        )
        return {
            "rule_name": rule_name,
            "rule_description": rule_desc,
            "impact": impact,
            "metric_improvement": improvement,
            "applied_prompt_snippet": snippet
        }

learning_agent = LearningAgentService()
