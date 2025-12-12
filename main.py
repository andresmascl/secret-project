from wakeword import WakeWordDetector
from recorder import Recorder
from stt_whisper_cpp import transcribe
from tts_piper import speak

wakeword = WakeWordDetector()
recorder = Recorder()

def main():
    speak("System ready. Say hey computer.")

    while True:
        wakeword.listen()

        speak("Yes?")
        audio = recorder.record()
        text = transcribe(audio)

        print("\n🟦 TRANSCRIBED:", text)
        speak(f"You said: {text}")

if __name__ == "__main__":
    main()
