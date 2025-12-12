# Scrapbot.AI Makefile

# -----------------------------
# Voicebot – Makefile
# -----------------------------

VENV := venv
WHISPER_DIR := whisper.cpp
WHISPER_BIN := $(WHISPER_DIR)/main
PIPX_BIN := $(HOME)/.local/bin

# Default target
all: setup

# -----------------------------
# 1. Create virtual environment
# -----------------------------
venv:
	python3 -m venv $(VENV)

# -----------------------------
# 2. Install Python dependencies
# -----------------------------
install: venv
	. $(VENV)/bin/activate && \
	pip install --upgrade pip && \
	pip install sounddevice soundfile numpy openwakeword silero-vad

# -----------------------------
# 3. Build whisper.cpp
# -----------------------------
whisper:
	test -d $(WHISPER_DIR) || git clone https://github.com/ggerganov/whisper.cpp
	$(MAKE) -C $(WHISPER_DIR) -j4

# -----------------------------
# 4. Download Whisper Base-Q5 model
# -----------------------------
models/ggml-base-q5_1.bin:
	mkdir -p models
	wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base-q5_1.bin -O models/ggml-base-q5_1.bin

# -----------------------------
# 5. Install Piper via pipx
# -----------------------------
piper:
	pip install pipx || true
	pipx install piper-tts || true

# -----------------------------
# 6. Download Piper voice
# -----------------------------
models/piper/en_US-amy-low.onnx:
	mkdir -p models/piper
	wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/low/en_US-amy-low.onnx -O models/piper/en_US-amy-low.onnx
	wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/low/en_US-amy-low.onnx.json -O models/piper/en_US-amy-low.onnx.json

# -----------------------------
# 7. Download wakeword model
# -----------------------------
models/openwakeword.tflite:
	mkdir -p models
	wget https://github.com/dscripka/openwakeword/releases/download/v0.5.0/hey_computer.tflite -O models/openwakeword.tflite

# -----------------------------
# 8. Full setup (everything)
# -----------------------------
setup: install whisper models/ggml-base-q5_1.bin models/piper/en_US-amy-low.onnx models/openwakeword.tflite
	@echo "✔ All components installed."

# -----------------------------
# 9. Run the assistant
# -----------------------------
run:
	. $(VENV)/bin/activate && python3 main.py

# -----------------------------
# 10. Clean build artifacts
# -----------------------------
clean:
	rm -rf $(WHISPER_DIR)/build
	rm -f $(WHISPER_BIN)

# -----------------------------
# 11. Clean everything
# -----------------------------
distclean: clean
	rm -rf $(VENV)
	rm -rf models

