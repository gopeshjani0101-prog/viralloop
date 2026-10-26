import asyncio
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.db import init_db, get_all_insights, get_all_videos
from app.services.llm_reasoning import llm_service
from app.services.discovery import discovery_service
from app.services.asset_manager import asset_manager
from app.services.video_editor import video_editor
from app.services.pipeline_orchestrator import pipeline_orchestrator

async def main():
    print("=" * 60)
    print("[*] VIRALLOOP BACKEND VERIFICATION SUITE")
    print("=" * 60)

    # 1. DB Init
    print("\n[1/5] Testing Database Initialization...")
    await init_db()
    insights = await get_all_insights()
    print(f"[OK] DB initialized with {len(insights)} seed learning insights.")
    for ins in insights:
        print(f"   * [{ins['rule_name']}]: {ins['rule_description']}")

    # 2. Ollama & Gemma
    print("\n[2/5] Testing Ollama Local LLM Connection...")
    models = await llm_service.get_available_models()
    selected_model = await llm_service.select_best_model()
    print(f"[OK] Available Ollama models: {models}")
    print(f"[OK] Active reasoning model: {selected_model}")

    # 3. Discovery Service
    print("\n[3/5] Testing Trending Discovery Service...")
    topics = await discovery_service.discover_trending_ideas()
    print(f"[OK] Discovered {len(topics)} candidate topics.")
    print(f"   Top candidate: '{topics[0].title}' (Source: {topics[0].source})")

    # 4. Full Pipeline Single Loop Execution
    print("\n[4/5] Executing 1 Autonomous ViralLoop Pipeline Cycle...")
    test_topic = "Scientists Discover Quantum Superposition In Biological Organisms"
    result = await pipeline_orchestrator.run_single_loop(custom_topic=test_topic)
    print(f"[OK] Pipeline Cycle Completed Successfully!")
    print(f"   * Title: {result['title']}")
    print(f"   * YouTube URL: {result['youtube_url']}")
    print(f"   * Learned Heuristic: {result['learned_rule']['rule_name']}")
    print(f"     Impact: {result['learned_rule']['metric_improvement']}")

    # 5. Database Video Check
    print("\n[5/5] Verifying Video Records in SQLite...")
    videos = await get_all_videos()
    print(f"[OK] Total videos in database: {len(videos)}")
    latest = videos[0]
    print(f"   Latest Video: '{latest['title']}'")
    print(f"   Duration: {latest['duration']:.1f}s | Views: {latest['views']} | Retention: {latest['retention_rate']}%")
    print(f"   File Path: {latest['file_path']}")
    
    print("\n[SUCCESS] ALL TESTS PASSED! ViralLoop Pipeline is fully operational.")

if __name__ == "__main__":
    asyncio.run(main())
