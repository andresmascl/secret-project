# main.py
import asyncio
import pyaudio
from listener import listen

# --------------------
# Audio Device
# --------------------
INPUT_DEVICE_INDEX = 3
RATE = 16000
CHANNELS = 1
FRAME_MS = 30
FRAME_SIZE = int(RATE * FRAME_MS / 1000)

def main():
    p = None
    stream = None

    try:
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=INPUT_DEVICE_INDEX,
            frames_per_buffer=FRAME_SIZE,
        )

        asyncio.run(listen(stream))

    except KeyboardInterrupt:
        print("\nStopping…")

    finally:
        if stream:
            stream.stop_stream()
            stream.close()
        if p:
            p.terminate()

if __name__ == "__main__":
    main()
