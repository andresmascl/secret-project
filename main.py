import os
import sys
import time
import queue
import threading
import sounddevice as sd
import soundfile as sf
from pynput import keyboard
from google.cloud import speech

# =========================
# CONFIG
# =========================

SAMPLE_RATE = 16000
CHANNELS = 1
AUDIO_FILE = "command.wav"

# Google STT
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials/google.json"

# =========================
# GLOBAL STATE
# =========================

audio_queue = queue.Queue()
recording = False
stream = None
frames = []

pressed_keys = set()
HOTKEY = {
    keyboard.Key.cmd,   # Super / Windows key
    keyboard.Key.alt,
    keyboard.Key.space
}

# =========================
# AUDIO RECORDING
# =========================

def audio_callback(indata, frames_count, time_info, status):
    if recording:
        frames.append(indata.copy())

def start_recording():
    global recording, stream, frames
    if recording:
        return

    print("🎙 Recording...")
    frames = []
    recording = True

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        callback=audio_callback
    )
    stream.start()

def stop_recording():
    global recording, stream
    if not recording:
        return

    print("🛑 Stopped recording")
    recording = False

    stream.stop()
    stream.close()

    sf.write(AUDIO_FILE, frames, SAMPLE_RATE)
    process_audio(AUDIO_FILE)

# =========================
# GOOGLE STT
# =========================

def google_stt(filename):
    client = speech.SpeechClient()

    with open(filename, "rb") as f:
        audio_bytes = f.read()

    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=SAMPLE_RATE,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    if not response.results:
        return ""

    return response.results[0].alternatives[0].transcript.strip()

# =========================
# LOCAL INTENT GUESSING
# =========================

def interpret_command(text):
    text = text.lower()
    print(f"🧠 Transcribed: {text}")

    if text.startswith("play"):
        return ("PLAY", text.replace("play", "").strip())

    if "pause" in text:
        return ("PAUSE", None)

    if "resume" in text:
        return ("RESUME", None)

    if "next" in text:
        return ("NEXT", None)

    return ("UNKNOWN", text)

# =========================
# LOCAL EXECUTION (STUB)
# =========================

def execute(intent, payload):
    print(f"⚙️ Executing: {intent}, {payload}")

    if intent == "PLAY":
        print(f"▶ Playing: {payload}")
        # TODO: Brave automation

    elif intent == "PAUSE":
        print("⏸ Pause")

    elif intent == "RESUME":
        print("▶ Resume")

    elif intent == "NEXT":
        print("⏭ Next")

    else:
        print("❓ Unknown command")

# =========================
# PIPELINE
# =========================

def process_audio(filename):
    text = google_stt(filename)
    if not text:
        print("⚠ No speech detected")
        return

    intent, payload = interpret_command(text)
    execute(intent, payload)

# =========================
# HOTKEY HANDLER
# =========================

def on_press(key):
    pressed_keys.add(key)
    if HOTKEY.issubset(pressed_keys):
        start_recording()

def on_release(key):
    if key in pressed_keys:
        pressed_keys.remove(key)
    if not HOTKEY.issubset(pressed_keys):
        stop_recording()

# =========================
# MAIN
# =========================

def main():
    print("🟢 Ready. Hold Super + Alt + Space to speak.")

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()
