# Use a Python 3.12 image (3.13 is still very new for some AI wheels)
FROM python:3.12-slim

# 1. Install system dependencies for PyAudio and PortAudio
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-dev \
    gcc \
    libasound2-plugins \
    && rm -rf /var/lib/apt/lists/*

# 2. Set up working directory
WORKDIR /app

# 3. Copy requirements and install
# We install torch CPU first to keep the image smaller
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of your code
COPY . .

# 5. Run as a non-root user (important for PulseAudio access)
# This assumes the host user ID is 1000
RUN useradd -m -u 1000 scrapbot
USER scrapbot

CMD ["python", "main.py"]