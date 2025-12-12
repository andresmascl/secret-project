# 🎤 Local Voice Assistant (Wake Word + Whisper.cpp + Piper TTS)
**This version contains ONLY the Makefile workflow + the project filemap.**

Everything—venv, dependencies, Whisper.cpp build, model downloads, and running—is done via the **Makefile**.

---

# 📁 Filemap

```
voicebot/
│── Makefile
│── main.py
│── wakeword.py
│── stt.py
│── tts.py
│── vad.py
│
├── whisper.cpp/               # auto-cloned + compiled
│   └── (build files)
│
├── models/
│   ├── ggml-base-q5_1.bin     # Whisper.cpp model
│   ├── openwakeword.tflite    # Wake word model
│   └── piper/
│       ├── en_US-amy-low.onnx
│       └── en_US-amy-low.onnx.json
│
└── venv/                      # virtual environment (created by Makefile)
```

---

# 🛠 Makefile Instructions

Below is the **full Makefile-driven workflow**.  
You do **NOT** manually install anything — the Makefile does it all.

---

## ✅ 1. Setup (ALL dependencies, venv, models, whisper.cpp)

```bash
make setup
```

This command:

- Creates a Python virtual environment (`venv/`)
- Installs Python dependencies
- Installs system libs (PortAudio, build tools)
- Clones & compiles Whisper.cpp
- Downloads:
  - Whisper Base-Q5 model
  - Wakeword model
  - Piper voice model
- Ensures microphone permissions
- Ensures `piper` is available

This installs everything needed in a single step.

---

## 🎤 2. Run the assistant

```bash
make run
```

This internally runs:

```
source venv/bin/activate && python3 main.py
```

You will hear:

```
System ready. Say hey computer.
```

---

## 🔧 3. Build Whisper.cpp manually

```bash
make whisper
```

---

## 📦 4. Download all models only

```bash
make models
```

Downloads:

- `ggml-base-q5_1.bin`
- `openwakeword.tflite`
- `piper` ONNX voice model

---

## 🧽 5. Clean build artifacts (keeps models)

```bash
make clean
```

---

## 💥 6. Full reset (remove venv + whisper.cpp + models)

```bash
make distclean
```

This returns the repo to a “fresh clone” state.

---

## 🎉 7. Ready!