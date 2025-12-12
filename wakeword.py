import sounddevice as sd
from openwakeword.model import Model

class WakeWordDetector:
    def __init__(self, threshold=0.55):
        self.model = Model(wakeword_models=["hey computer"])
        self.threshold = threshold

    def listen(self):
        """Block until wake word is detected."""
        with sd.InputStream(channels=1, samplerate=16000, dtype='float32') as stream:
            while True:
                audio = stream.read(16000)[0].flatten()
                scores = self.model.predict(audio)
                if scores[0]["hey computer"] > self.threshold:
                    print("Wake word detected!")
                    return True
