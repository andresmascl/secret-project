# config.py
import os 
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# 1. Setup Paths and Load Env
load_dotenv(find_dotenv())

# ---------------------------------------------------------
# 2. AUDIO & LISTENER SETTINGS
# ---------------------------------------------------------
# Live API recommends 16kHz for input to minimize bandwidth/latency
AUDIO_RATE = 16000
CHANNELS = 1
# 1280 frames at 16kHz is ~80ms of audio, ideal for real-time streaming
FRAME_SIZE = 1024

# Wake word settings
WAKE_KEY = "hey_mycroft"
WAKE_THRESHOLD = 0.6
WAKE_RESET_THRESHOLD = 0.2
WAKE_COOLDOWN_SEC = 3.0

# VAD (Voice Activity Detection) settings
SILENCE_SECONDS = 1
MIN_SPEECH_SECONDS = 0.3
VAD_THRESHOLD = 0.5

# ---------------------------------------------------------
# 3. GOOGLE CLOUD / LIVE API SETTINGS
# ---------------------------------------------------------
# Credentials and Project ID for Vertex AI
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
REGION = os.getenv("GCP_REGION", "us-central1")
MODEL_NAME = os.getenv("VERTEX_MODEL_NAME", "gemini-2.0-flash")

# New Live API Specifics
LIVE_API_VOICE = "Aoede" # Options: Puck, Charon, Kore, Fenrir, Aoede
SYSTEM_INSTRUCTION = (
    "You are Scrapbot, a helpful robotic assistant. Respond in a friendly, "
    "concise manner. If a user asks to move the robot, use your tools. "
    "If information is missing, ask for it."
)
