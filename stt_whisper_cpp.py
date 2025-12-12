import subprocess
import numpy as np
import tempfile
import wave
import os

WHISPER_BIN = "./whisper.cpp/main"
WHISPER_MODEL = "models/ggml-base-q5_1.bin"

def transcribe(audio_float32):
    """Convert audio to WAV and run whisper.cpp."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        wav_path = f.name

    # Save audio
    with wave.open(wav_path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        w.writeframes((audio_float32 * 32767).astype(np.int16).tobytes())

    result = subprocess.run(
        [WHISPER_BIN, "-m", WHISPER_MODEL, "-f", wav_path, "--no-timestamps"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    os.remove(wav_path)

    return result.stdout.strip().split("\n")[-1]
