import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
VENV_PYTHON = ROOT_DIR / "venv" / "Scripts" / "python.exe"

if not VENV_PYTHON.exists():
    print(f"Error: Python virtual environment not found at {VENV_PYTHON}")
    sys.exit(1)

def main():
    print("=" * 65)
    print("🚀 LAUNCHING VIRALLOOP - AUTONOMOUS VIRAL VIDEO AGENT")
    print("=" * 65)
    print("Backend URL:   http://localhost:8000")
    print("API Docs:      http://localhost:8000/docs")
    print("Ollama Engine: Localhost:11434 (Gemma 4)")
    print("=" * 65)

    # Launch Backend Server
    backend_cmd = [str(VENV_PYTHON), "backend/run_backend.py"]
    server_proc = subprocess.Popen(backend_cmd, cwd=str(ROOT_DIR))

    # Give server a moment to start
    time.sleep(2)
    webbrowser.open("http://localhost:8000")

    try:
        server_proc.wait()
    except KeyboardInterrupt:
        print("\nShutting down ViralLoop...")
        server_proc.terminate()
        server_proc.wait()

if __name__ == "__main__":
    main()
