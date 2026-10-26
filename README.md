# 🚀 ViralLoop: Autonomous Viral Content Pipeline & Self-Improving Agent

**ViralLoop** is a production-grade, demo-ready autonomous AI pipeline that continuously:
1. **Discovers** trending content ideas from live web sources (Reddit, Hacker News, Google Trends).
2. **Reasons** using a local LLM (**Gemma 4 via Ollama**) to pick winning topics, score virality, craft 3-second retention hooks, and write loop-transition scripts.
3. **Downloads & Assembles** neural voiceover (Edge-TTS) and high-resolution 1080x1920 vertical background loops with millisecond word sync.
4. **Edits** complete vertical videos with **FFmpeg**, burning in high-contrast, bold yellow/white English subtitles (TikTok / Shorts style) and faststart MP4 encoding.
5. **Posts** them to **YouTube Shorts** (with dual-mode support: Live YouTube Data API v3 OAuth or instant realistic Simulation Mode).
6. **Learns** from video analytics (viewer retention %, completion rate, likes, comments) and updates the local agent's system prompt memory with newly synthesized viral heuristics for each subsequent video.

---

## ⚡ Quick Start (Run in 1 Step)

```bash
# 1. Double-click or run:
start.bat

# Or run via Python:
.\venv\Scripts\python run_viralloop.py
```
Open **`http://localhost:8000`** in your browser.

---

## 🛠️ System Architecture

```
                                    VIRALLOOP SYSTEM PIPELINE
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                             │
│  [1. DISCOVERY] ───────► [2. GEMMA 4 REASONING] ───────► [3. VOICE & ASSETS]                │
│   - Reddit (r/tech, etc.)  - Virality Scoring (1-100)      - Edge-TTS Neural Speech         │
│   - HackerNews Top         - 3s Retention Hook             - 1080x1920 Generative Loops     │
│   - Google Trends RSS      - 30-45s Loop Script            - Word-Level Subtitle Timings    │
│                                                                        │                    │
│  [6. BRAIN MEMORY] ◄─── [5. YOUTUBE SHORTS] ◄──────── [4. FFMPEG COMPOSITOR]               │
│   - Retention Analytics    - Live OAuth / Simulator Mode    - 9:16 Vertical Video           │
│   - Evolutionary Lessons   - Metatags & Viral Thumbnail     - Styled Burned-in Subtitles    │
│   - Dynamic System Prompt  - Viewer Growth Curves           - Faststart Streaming MP4       │
│                                                                                             │
└──────────────────────────────────────────────┬──────────────────────────────────────────────┘
                                               │
                                               ▼
                              REACT + VITE STUDIO DASHBOARD
             - Live 5-Stage Animated Pipeline Stepper with Real-Time Telemetry
             - Built-in Vertical (9:16) Shorts Player & Gallery
             - Channel Performance Analytics & Views Velocity Chart
             - "Agent Brain" Memory Inspector (View heuristics evolved across iterations)
```

---

## 🧠 Local LLM Reasoning (Ollama & Gemma 4)

ViralLoop uses local Ollama at `http://localhost:11434` for 100% private, zero-cost AI reasoning:
- **Configured Model**: `gemma4` (or `gemma:2b`, `qwen2.5:3b`)
- **Self-Improving Reinforcement Loop**:
  - After each video is published, viewer retention is measured against channel benchmarks.
  - Gemma 4 reflects on the script structure and derives a new tactical viral rule (e.g., *"Urgency Escalation Hook: Introduce consequence in first 1.8 seconds"*).
  - The rule is stored in SQLite and automatically injected into subsequent generation prompts!

---

## 📺 YouTube Shorts Publishing Modes

Configured in `.env` or switched live from the UI Settings:
- **`simulated` (Default for Hackathon Demos)**: Generates instant YouTube Shorts URLs (`https://www.youtube.com/shorts/{id}`), valid video records, and realistic organic view/retention growth curves without requiring API quotas or manual OAuth authorization.
- **`live`**: Uses official YouTube Data API v3 OAuth (`client_secrets.json` & `token.json`) to publish directly to your verified YouTube channel.

---

## 📁 Project Structure

```
├── backend/
│   ├── app/
│   │   ├── config.py                 # Application settings (.env loader)
│   │   ├── db.py                     # SQLite database & CRUD operations
│   │   ├── models.py                 # Pydantic models & data schemas
│   │   ├── services/
│   │   │   ├── discovery.py          # Trending content discovery service
│   │   │   ├── llm_reasoning.py      # Ollama Gemma 4 reasoning engine
│   │   │   ├── asset_manager.py      # Edge-TTS voiceover & asset generator
│   │   │   ├── video_editor.py       # FFmpeg 9:16 vertical video & captions compositor
│   │   │   ├── youtube_publisher.py  # Live / Simulator YouTube Shorts publisher
│   │   │   ├── analytics_collector.py# Performance metric scraper & growth simulator
│   │   │   ├── learning_agent.py     # Evolutionary feedback loop & rule synthesizer
│   │   │   └── pipeline_orchestrator.py # Master autonomous loop coordinator
│   │   ├── routes/                   # FastAPI REST API endpoints
│   │   └── main.py                   # FastAPI server & React static mounting
│   ├── storage/                      # Rendered videos, audio, and subtitles
│   ├── tests/
│   │   └── test_backend.py           # End-to-end verification suite
│   ├── viralloop.db                  # Persistent SQLite database
│   ├── requirements.txt
│   └── run_backend.py
├── frontend/
│   ├── src/
│   │   ├── components/               # Navbar, PipelineVisualizer, VideoCard, etc.
│   │   ├── services/api.js           # API communication client
│   │   ├── App.jsx                   # Main React dashboard shell
│   │   └── index.css                 # Tailwind CSS styling
│   ├── package.json
│   └── vite.config.js
├── run_viralloop.py                  # 1-click full stack launcher
├── start.bat                         # Windows batch launcher
├── .env.example                      # Configuration template
└── README.md
```

---

## 🧪 Verification & Testing

To run the automated verification suite:
```bash
.\venv\Scripts\python backend/tests/test_backend.py
```
This tests:
1. SQLite database initialization & seed heuristics
2. Ollama connection & Gemma 4 availability
3. Trend discovery from live feeds
4. Full autonomous cycle (audio synthesis, FFmpeg rendering, YouTube publishing, learning reflection)
5. SQLite video record verification

---

## 🏆 Hackathon Demo Flow
1. Run `start.bat`.
2. Open `http://localhost:8000`.
3. In the **Studio** tab, click **"Run Single Loop"** (or type a custom topic e.g. *"AI Discovered A Secret Language"*).
4. Watch the 5 stages animate in real time on the visualizer and observe the terminal telemetry.
5. Watch the celebration confetti burst as the 9:16 Short finishes rendering!
6. Click **"Play Short"** to watch the vertical video directly with burned-in subtitles and synchronized neural audio.
7. Click the **"Brain Memory"** tab to see the newly learned viral heuristic that Gemma extracted from the video's statistics!
