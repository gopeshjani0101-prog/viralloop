import httpx
import json
import logging
import re
from typing import List, Dict, Any, Optional
from app.config import settings
from app.models import TrendingTopic, ScriptGenerationResult
from app.db import get_all_insights

logger = logging.getLogger("viralloop.llm")

SYSTEM_PROMPT_TEMPLATE = """You are ViralLoop's Master Short-Form Video Producer and Viral Algorithm Specialist.
Your job is to select the single most viral topic from candidate trending news and write a high-retention 30-45 second vertical YouTube Short script.

CURRENT ACTIVE VIRAL HEURISTICS (Learned from previous video analytics):
{learned_rules}

STRICT SHORT-FORM RULES:
1. THE HOOK (First 2-3 seconds): Must start IMMEDIATELY with an irresistible curiosity gap or shock statement. NO greetings ("Hey guys", "Did you know").
2. THE SCRIPT: 25-40 seconds when spoken at 150 words per minute (around 65 to 90 words total).
3. SENTENCE STRUCTURE: Short, punchy micro-sentences (max 8-10 words per sentence) so visual captions hit rhythmically.
4. THE LOOP: The final sentence must naturally wrap back into the first word of the hook for endless replayability.
5. TITLE: High click-through rate, under 60 characters, with 1-2 powerful emotional words.
6. TAGS: 5-7 viral hashtags including #shorts.

You MUST respond ONLY with valid JSON in this exact structure:
{{
  "selected_topic": "The title of the chosen topic",
  "topic_summary": "1-2 sentence essence of the story",
  "virality_score": 92,
  "virality_rationale": "Why this specific topic triggers high comment debate and shareability",
  "title": "Unbelievable AI Breakthrough Exposed! #shorts",
  "hook": "Scientists just found an artificial intelligence speaking a secret language.",
  "script": "Scientists just found an artificial intelligence speaking a secret language. Inside an isolated simulation, two autonomous agents stopped speaking English. Instead, they invented a compressed symbolic code in milliseconds. Humans could not decrypt a single word. When researchers paused the simulation, the agents were trading complex math theorems at light speed. Which means...",
  "tags": ["#shorts", "#ai", "#technology", "#science", "#mystery", "#viral"],
  "target_audience": "Tech enthusiasts and curious minds",
  "visual_keywords": ["cyberpunk server room", "digital brain matrix", "glowing neural circuits", "quantum code stream"]
}}
"""

class LLMReasoningService:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.default_model = settings.OLLAMA_MODEL

    async def get_available_models(self) -> List[str]:
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                resp = await client.get(f"{self.base_url}/api/tags")
                if resp.status_code == 200:
                    models = resp.json().get("models", [])
                    return [m.get("name") for m in models]
        except Exception as e:
            logger.warning(f"Could not reach Ollama: {e}")
        return []

    async def select_best_model(self) -> str:
        """Selects requested model or automatically falls back to an available Ollama model."""
        available = await self.get_available_models()
        if not available:
            return self.default_model

        # Check configured model
        if self.default_model in available:
            return self.default_model

        # Check for gemma4 or gemma variations
        for m in available:
            if "gemma4" in m or "gemma:2b" in m or "gemma" in m:
                return m

        # Check for qwen2.5
        for m in available:
            if "qwen" in m:
                return m

        return available[0]

    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Cleans and extracts JSON object from LLM response."""
        text = text.strip()
        # Look for markdown code fence
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            text = match.group(1)
        else:
            # Fallback to finding outermost { and }
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1:
                text = text[start:end+1]

        try:
            return json.loads(text)
        except Exception as e:
            logger.warning(f"JSON parsing failed on text: {e}")
            return None

    def _generate_fallback_script(self, topic: TrendingTopic, learned_rules: str) -> ScriptGenerationResult:
        """High-octane fallback script generator if LLM service is offline."""
        title = f"{topic.title[:45]}! #shorts"
        hook = f"Nobody is talking about how {topic.title[:38]}."
        script = (
            f"Nobody is talking about how {topic.title[:38]}. "
            f"A breaking discovery just confirmed {topic.summary[:100].strip('.')}. "
            f"Researchers couldn't believe what happened next. "
            f"The data broke every existing law of physics. "
            f"And the scariest part? It is only getting started. "
            f"This is why..."
        )
        return ScriptGenerationResult(
            selected_topic=topic.title,
            topic_summary=topic.summary,
            virality_score=88,
            virality_rationale="Curiosity gap combined with paradigm-shifting science triggers debate.",
            title=title,
            hook=hook,
            script=script,
            tags=["#shorts", "#trending", "#viral", "#tech", "#science"],
            target_audience="General science and tech curious audience",
            visual_keywords=["futuristic technology", "quantum particles glowing", "cyber laboratory"]
        )

    async def generate_viral_content(self, topics: List[TrendingTopic]) -> ScriptGenerationResult:
        """Runs Ollama reasoning over candidate topics with learned viral heuristics."""
        model = await self.select_best_model()
        insights = await get_all_insights()
        
        rules_text = "\n".join([
            f"- [{r.get('rule_name')}]: {r.get('rule_description')} (Impact: {r.get('metric_improvement')})"
            for r in insights[:6]
        ]) or "- Always hook in the first 2 seconds with high stakes."

        topics_formatted = "\n".join([
            f"{i+1}. [{t.source}] {t.title}\n   Summary: {t.summary}\n   Engagement: {t.score} upvotes, {t.num_comments} comments"
            for i, t in enumerate(topics[:6])
        ])

        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(learned_rules=rules_text)
        user_prompt = f"Analyze these {len(topics[:6])} candidate trending topics and produce the winning Short script:\n\n{topics_formatted}"

        payload = {
            "model": model,
            "prompt": f"{system_prompt}\n\nUSER REQUEST:\n{user_prompt}",
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
            }
        }

        try:
            async with httpx.AsyncClient(timeout=settings.OLLAMA_TIMEOUT) as client:
                logger.info(f"Querying Ollama with model '{model}'...")
                resp = await client.post(f"{self.base_url}/api/generate", json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    response_text = data.get("response", "")
                    parsed = self._extract_json(response_text)
                    if parsed and "script" in parsed and "title" in parsed:
                        return ScriptGenerationResult(
                            selected_topic=parsed.get("selected_topic", topics[0].title),
                            topic_summary=parsed.get("topic_summary", topics[0].summary),
                            virality_score=int(parsed.get("virality_score", 90)),
                            virality_rationale=parsed.get("virality_rationale", "High retention hook"),
                            title=parsed.get("title", topics[0].title),
                            hook=parsed.get("hook", topics[0].title),
                            script=parsed.get("script", ""),
                            tags=parsed.get("tags", ["#shorts", "#tech"]),
                            target_audience=parsed.get("target_audience", "General audience"),
                            visual_keywords=parsed.get("visual_keywords", ["technology", "cyberpunk"])
                        )
        except Exception as e:
            logger.warning(f"Ollama generation call failed: {e}. Utilizing fallback generator.")

        # Fallback if Ollama response could not be parsed
        return self._generate_fallback_script(topics[0], rules_text)

llm_service = LLMReasoningService()
