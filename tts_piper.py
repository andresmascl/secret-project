import subprocess
import tempfile
import sounddevice as sd
import soundfile as sf

PIPER_BIN = "piper"   # Must be in PATH
PIPER_MODEL = "models/piper/en_US-amy-low.onnx"

def speak(text):
    """Generate TTS using Piper and play audio."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        wav_path = f.name

    # Run piper
    subprocess.run(
        [PIPER_BIN, "-m", PIPER_MODEL, "-f", wav_path],
        input=text.encode("utf8")
    )

    # Play
    audio, sr = sf.read(wav_path, dtype="float32")
    sd.play(audio, sr)
    sd.wait()
