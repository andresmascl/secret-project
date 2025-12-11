import openai
import os
from dotenv import load_dotenv
from computer_use import run_claude

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def read_audio_npy(path):
    import numpy as np
    return np.load(path).astype("float32")

def transcribe_and_forward(path):
    print("🔍 Transcribing with Whisper...")

    audio = read_audio_npy(path)

    client = openai.OpenAI()

    # Save WAV temporary for API requirement
    import soundfile as sf
    wav_path = "temp.wav"
    sf.write(wav_path, audio, 16000)

    with open(wav_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-tts",
            file=f
        )

    text = transcript.text
    print("📝 Whisper text:", text)

    print("🖥 Sending to Claude Computer Use…")
    run_claude(text)