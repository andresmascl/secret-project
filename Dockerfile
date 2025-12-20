# Dockerfile updates
FROM python:3.12-slim

# 1. Added ffmpeg for playback and libpulse0 for PulseAudio support
RUN apt-get update && apt-get install -y --no-install-recommends \
    portaudio19-dev \
    python3-dev \
    gcc \
    libasound2-plugins \
    ffmpeg \
    libpulse0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV TORCH_HOME=/home/scrapbot/.cache/torch

COPY requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade pip setuptools && \
    python -m pip install --no-cache-dir -r requirements.txt

RUN python3 -c "import torch; torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', force_reload=True, trust_repo=True)"

# 2. Copy code AND your sound file
COPY . .

RUN useradd -m -u 1000 scrapbot && \
    mkdir -p /home/scrapbot/.cache/torch && \
    chown -R scrapbot:scrapbot /home/scrapbot /app

USER scrapbot

CMD ["python", "main.py"]