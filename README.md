## README – Local Voice Assistant (Wake Word + STT + TTS)

#### This project provides a fully offline voice assistant for Linux using:

##### OpenWakeWord → wake-word detection

##### Silence cutoff → automatic end-of-speech

##### Whisper.cpp (Base-Q5) → fast speech-to-text

##### Piper TTS → fast, fully local text-to-speech

Works well on low-spec hardware (e.g., 8GB RAM + Pentium N3710).


## 📦 Project Structure
```bash
voicebot/
│── main.py
│── wakeword.py
│── stt.py
│── tts.py
│── vad.py
│── Makefile
│
├── models/
│   ├── ggml-base-q5_1.bin
│   ├── openwakeword.tflite
│   └── piper/
│       ├── en_US-amy-low.onnx
│       └── en_US-amy-low.onnx.json
│
└── whisper.cpp/
    └── (compiled binaries)
```

## 🚀 Setup Instructions
✅ 1. Install system dependencies
```bash
sudo apt update
sudo apt install -y build-essential python3-pip python3-venv \
    portaudio19-dev libsndfile1 ffmpeg
```

✅ 2. Create virtual environment
```bash
cd voicebot
python3 -m venv venv
source venv/bin/activate
```

✅ 3. Install Python dependencies
```bash
pip install sounddevice soundfile numpy openwakeword silero-vad
```

✅ 4. Build Whisper.cpp
```bash
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
make -j4
cd ..
```

✅ 5. Download Whisper Base-Q5 model
```bash
mkdir -p models
cd models
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base-q5_1.bin
cd ..
```

✅ 6. Install Piper TTS
```bash
pip install pipx
pipx install piper-tts
```

Download the voice model:

```bash
mkdir -p models/piper
cd models/piper
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/low/en_US-amy-low.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/low/en_US-amy-low.onnx.json
cd ../..
```

✅ 7. Download OpenWakeWord model
```bash
mkdir -p models
cd models
wget https://github.com/dscripka/openwakeword/releases/download/v0.5.0/hey_computer.tflite -O openwakeword.tflite
cd ..
```

🎤 8. Give microphone permissions (Linux)
```bash
sudo usermod -aG audio $USER
sudo usermod -aG pulse $USER
```


Reboot after this.

🧪 Running the Project

Activate the venv:

```bash
source venv/bin/activate
```

Then run:

```bash
python3 main.py
```

You should hear:
```bash
System ready. Say hey computer.
```

Say “hey computer”:

Wake word triggers

You speak

Silence cutoff ends recording

Whisper transcribes

Piper speaks back the response

## 🛠 Using the Makefile

▶ Full installation
```bash
make setup
```
▶ Run the assistant
```bash
make run
```
▶ Build Whisper.cpp only
```bash
make whisper
```
▶ Download all models

(Handled automatically by setup, but can be done manually)
```bash
make models/ggml-base-q5_1.bin
make models/openwakeword.tflite
make models/piper/en_US-amy-low.onnx
```
▶ Reset build artifacts
```bash
make clean
```
▶ Delete everything including venv + models
```bash
make distclean
```
🚨 Troubleshooting
❌ Wakeword not triggering

Check microphone:

```bash
python3 - <<EOF
import sounddevice as sd
print(sd.query_devices())
EOF
```

Make sure your default input device exists and is not muted.

❌ Whisper binary not found

Ensure the path matches:

```bash
WHISPER_BIN = "./whisper.cpp/main"
```
❌ Piper command not found

Add pipx to PATH:
```bash
echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc
source ~/.bashrc
```