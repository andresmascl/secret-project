# listener.py
import asyncio
import numpy as np
import wave
import time
import torch
from openwakeword.model import Model

from configs.listener_config import (
    AUDIO_RATE, # 16000
    CHANNELS,
    WAKE_KEY,
    WAKE_THRESHOLD,
    WAKE_RESET_THRESHOLD,
    WAKE_COOLDOWN_SEC,
    SILENCE_SECONDS,
    MIN_SPEECH_SECONDS,
)

# --------------------
# Derived constants
# --------------------
FRAME_SIZE = 1024 

# --------------------
# Models
# --------------------
print("Loading Silero VAD and Wake Word models...", flush=True)
wake_model = Model() 

vad_model, _ = torch.hub.load(
    repo_or_dir='snakers4/silero-vad', 
    model='silero_vad', 
    force_reload=False,
    trust_repo=True  
)

def save_wav(frames, filename):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(AUDIO_RATE) 
        wf.writeframes(b"".join(frames))

# --------------------
# Public API
# --------------------
async def listen(stream, native_rate, on_audio_recorded=None):
    print(f"🎙️ Resampling Engine: {native_rate}Hz -> {AUDIO_RATE}Hz", flush=True)
    print(f"👂 Listening for wake word '{WAKE_KEY}'...", flush=True)
    
    # Pre-print an empty line so the first cursor-up move has a target
    print("", flush=True)
    
    VAD_WINDOW = 512
    vad_processing_buffer = np.array([], dtype=np.int16)

    recording = False
    speech_started = False
    wake_armed = True
    audio_buffer = []
    last_record_end = 0
    last_heartbeat = time.time()
    
    is_speech_global = False
    silence_start_time = None
    speech_start_time = None

    while True:
        await asyncio.sleep(0)
        
        try:
            data = stream.read(FRAME_SIZE, exception_on_overflow=False)
            if not data:
                continue
            audio_int16 = np.frombuffer(data, dtype=np.int16)
            
            # --- DYNAMIC PROGRESS BAR (Single Line in Docker) ---
            if time.time() - last_heartbeat > 0.15: 
                rms = np.sqrt(np.mean(audio_int16.astype(np.float32)**2))
                
                # Use a sensitivity threshold so we don't flicker on absolute silence
                if rms > 80:
                    bar_length = min(20, int(rms / 100))
                    icon = "🔊" if is_speech_global else "🎙️"
                    progress_bar = icon + "█" * bar_length + "░" * (20 - bar_length)
                    
                    # \033[F moves cursor UP one line
                    # \033[K clears the line from cursor to end
                    # This allows us to overwrite the previous Docker-prefixed line
                    print(f"\033[F\033[K{progress_bar} [Vol: {rms:5.0f}]", flush=True)
                
                last_heartbeat = time.time()
            
            # --- RESAMPLING ---
            if native_rate != AUDIO_RATE:
                num_samples = len(audio_int16)
                target_num_samples = int(num_samples * AUDIO_RATE / native_rate)
                audio_int16_16k = np.interp(
                    np.linspace(0, 1, target_num_samples),
                    np.linspace(0, 1, num_samples),
                    audio_int16
                ).astype(np.int16)
            else:
                audio_int16_16k = audio_int16
            
            vad_processing_buffer = np.append(vad_processing_buffer, audio_int16_16k)

            while len(vad_processing_buffer) >= VAD_WINDOW:
                current_chunk = vad_processing_buffer[:VAD_WINDOW]
                vad_processing_buffer = vad_processing_buffer[VAD_WINDOW:]
                
                audio_float32 = current_chunk.astype(np.float32) / 32768.0
                now = time.time()

                # --- VAD ---
                speech_prob = vad_model(torch.from_numpy(audio_float32), AUDIO_RATE).item()
                is_speech = speech_prob > 0.45 
                is_speech_global = is_speech 

                # --- WAKE WORD ---
                if not recording:
                    preds = wake_model.predict(current_chunk)
                    score = 0.0
                    for k, v in preds.items():
                        if WAKE_KEY in k:
                            score = v
                            break

                    if score < WAKE_RESET_THRESHOLD:
                        wake_armed = True

                    if wake_armed and score >= WAKE_THRESHOLD and (now - last_record_end) > WAKE_COOLDOWN_SEC:
                        # Print a newline to "escape" the heartbeat line before the event log
                        print(f"\n✨ WAKE WORD DETECTED ({score:.2f}) ✨", flush=True)
                        # Re-print an empty line to reset the heartbeat's "overwriting" target
                        print("", flush=True)
                        recording, speech_started = True, False
                        audio_buffer = []
                        wake_armed = False

                if recording:
                    audio_buffer.append(current_chunk.tobytes())
                    if is_speech:
                        if speech_start_time is None: speech_start_time = now
                        silence_start_time = None 
                        if not speech_started and (now - speech_start_time) >= MIN_SPEECH_SECONDS:
                            speech_started = True
                    else:
                        if silence_start_time is None: silence_start_time = now
                        if speech_started and (now - silence_start_time) >= SILENCE_SECONDS:
                            print("\n🛑 Utterance finished. Processing...", flush=True)
                            print("", flush=True) # Reset heartbeat target
                            filename = f"/tmp/recording_{int(time.time())}.wav"
                            save_wav(audio_buffer, filename)
                            if on_audio_recorded:
                                await on_audio_recorded(filename)
                            recording, speech_started = False, False
                            speech_start_time, silence_start_time = None, None
                            last_record_end = time.time()
        except Exception as e:
            print(f"\n⚠️ Loop Error: {e}", flush=True)
            print("", flush=True)
