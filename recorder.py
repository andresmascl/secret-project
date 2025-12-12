import sounddevice as sd
import numpy as np
from silero_vad import SileroVAD

class Recorder:
    def __init__(self, silence_ms=900):
        self.vad = SileroVAD()
        self.silence_ms = silence_ms

    def record(self):
        samplerate = 16000
        audio_frames = []
        silence_start = None

        print("Speak now…")

        with sd.InputStream(channels=1, samplerate=samplerate, dtype='float32') as stream:
            while True:
                frame = stream.read(1600)[0].flatten()
                audio_frames.append(frame)

                speech = self.vad.predict(frame, samplerate)

                if speech < 0.1:  
                    if silence_start is None:
                        silence_start = sd.get_stream_time(stream)
                    elif (sd.get_stream_time(stream) - silence_start) * 1000 > self.silence_ms:
                        print("Silence detected, stopping.")
                        break
                else:
                    silence_start = None

        return np.concatenate(audio_frames)
