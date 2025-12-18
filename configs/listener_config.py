# listener_config.py

# --------------------
# Audio
# --------------------
AUDIO_RATE = 16000
CHANNELS = 1
FRAME_SIZE = 1536
# --------------------
# Wake word
# --------------------
WAKE_KEY = "hey_mycroft"
WAKE_THRESHOLD = 0.6
WAKE_RESET_THRESHOLD = 0.2
WAKE_COOLDOWN_SEC = 3.0

# --------------------
# Voice Activity Detection (VAD)
# --------------------
VAD_MODE = 2                 # 0 = permissive, 3 = aggressive
SILENCE_SECONDS = 0.8        # stop after this much non-speech
MIN_SPEECH_SECONDS = 0.3     # gate: require actual speech
VAD_THRESHOLD = 0.5  # Confidence threshold for speech (0.0 to 1.0)