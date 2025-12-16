import pyaudio
import webrtcvad
import numpy as np
import asyncio
from sentence_transformers import SentenceTransformer, util

# --------------------
# Configuration
# --------------------
RATE = 16000
FRAME_DURATION_MS = 30
FRAME_SIZE = int(RATE * FRAME_DURATION_MS / 1000)
SILENCE_FRAMES_TO_STOP = 20  # ~600ms of silence to consider end of command
WAKE_WORD = "Ok House"

# --------------------
# Models
# --------------------
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
wake_embedding = embedding_model.encode(WAKE_WORD, normalize_embeddings=True)

vad = webrtcvad.Vad(2)  # 0–3 (aggressiveness)

# --------------------
# Audio Setup
# --------------------
audio = pyaudio.PyAudio()
stream = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAME_SIZE,
)

# --------------------
# Helpers
# --------------------
def is_speech(frame: bytes) -> bool:
    return vad.is_speech(frame, RATE)

def bytes_to_np(audio_bytes: bytes) -> np.ndarray:
    return np.frombuffer(audio_bytes, dtype=np.int16)

def semantic_wake_detect(text: str, threshold=0.6) -> bool:
    emb = embedding_model.encode(text, normalize_embeddings=True)
    score = util.cos_sim(emb, wake_embedding).item()
    return score >= threshold

# --------------------
# Main Loop
# --------------------
async def listen():
    print("🎙️ Listening...")

    speech_buffer = []
    silence_count = 0
    triggered = False

    while True:
        frame = stream.read(FRAME_SIZE, exception_on_overflow=False)

        if is_speech(frame):
            speech_buffer.append(frame)
            silence_count = 0
        else:
            silence_count += 1

        # End of utterance
        if speech_buffer and silence_count > SILENCE_FRAMES_TO_STOP:
            audio_np = bytes_to_np(b"".join(speech_buffer))
            speech_buffer.clear()
            silence_count = 0

            # ---- PLACEHOLDER ----
            # Here you would call STT
            # For now, fake text input
            text = input("Simulated STT text: ").lower()

            if not triggered:
                if semantic_wake_detect(text):
                    triggered = True
                    print("🟢 Wake word detected")
                else:
                    print("🔕 Ignored (no wake word)")
            else:
                print(f"📨 Command received: {text}")
                triggered = False

        await asyncio.sleep(0)

# --------------------
# Entry Point
# --------------------
if __name__ == "__main__":
    try:
        asyncio.run(listen())
    except KeyboardInterrupt:
        print("\nStopping...")
        stream.stop_stream()
        stream.close()
        audio.terminate()