import asyncio
import json
import os
import sys
import subprocess
import numpy as np
import torch
from google import genai
from google.genai import types
from config import PROJECT_ID
import listener  # Access vad_model from listener

# Configuration
LOCATION = "us-central1"
MODEL_ID = "gemini-2.0-flash-live"
SILENCE_THRESHOLD_MS = 1500  # Stop streaming after 1.5s of silence

def get_system_instruction():
    try:
        with open("PROMPT.md", "r") as f:
            return f.read()
    except FileNotFoundError:
        print("⚠️ PROMPT.md not found. Using default instruction.")
        return "You are a helpful assistant."

async def run_live_session(audio_gen):
    """
    Connects to Vertex AI Multimodal Live API, streams audio, 
    detects silence to stop recording, and prints the JSON response.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print(f"🔑 Using Google AI Studio API Key with {MODEL_ID}...", flush=True)
        client = genai.Client(api_key=api_key, http_options={'api_version': 'v1beta1'})
    else:
        print(f"⚡ Connecting to Vertex AI with {MODEL_ID}...", flush=True)
        client = genai.Client(project=PROJECT_ID, location=LOCATION, http_options={'api_version': 'v1beta1'})

    system_instruction = get_system_instruction()
    
    # VAD State
    silence_start_time = None
    is_speaking = False
    
    print(f"⚡ Connecting to {MODEL_ID}...", flush=True)

    config = types.LiveConnectConfig(
        response_modalities=["TEXT"],
        system_instruction=types.Content(parts=[types.Part(text=system_instruction)]),
    )

    async with client.aio.live.connect(model=MODEL_ID, config=config) as session:
        print("🔴 Live Session Started. Speak now!", flush=True)
        
        accumulated_response = ""
        
        async def send_audio_loop():
            nonlocal silence_start_time, is_speaking
            vad_buffer = b""
            
            try:
                async for chunk in audio_gen:
                    # 1. Send Audio to API
                    await session.send(input={"data": chunk, "mime_type": "audio/pcm"}, end_of_turn=False)
                    
                    # 2. Local VAD Logic to detect "Stop"
                    vad_buffer += chunk
                    
                    # Silero VAD requires chunks of 512, 1024, or 1536 samples (at 16kHz).
                    # 512 samples * 2 bytes/sample = 1024 bytes.
                    while len(vad_buffer) >= 1024:
                        process_chunk = vad_buffer[:1024]
                        vad_buffer = vad_buffer[1024:]

                        # Convert int16 bytes to float32 tensor for Silero VAD
                        audio_int16 = np.frombuffer(process_chunk, dtype=np.int16)
                        audio_float32 = audio_int16.astype(np.float32) / 32768.0
                        tensor = torch.from_numpy(audio_float32)
                        
                        # Get speech probability
                        speech_prob = listener.vad_model(tensor, 16000).item()
                        
                        if speech_prob > 0.5:
                            is_speaking = True
                            silence_start_time = None
                            sys.stdout.write(".") # Visual feedback for speech
                            sys.stdout.flush()
                        else:
                            if is_speaking: # Only count silence if we have started speaking
                                if silence_start_time is None:
                                    silence_start_time = asyncio.get_running_loop().time()
                                
                                elapsed_silence = (asyncio.get_running_loop().time() - silence_start_time) * 1000
                                if elapsed_silence > SILENCE_THRESHOLD_MS:
                                    print("\n🛑 Silence detected. Processing response...", flush=True)
                                    await session.send(input=None, end_of_turn=True)
                                    return
            except Exception as e:
                print(f"Error in send_audio_loop: {e}")

        async def receive_loop():
            nonlocal accumulated_response
            async for response in session.receive():
                server_content = response.server_content
                if server_content and server_content.model_turn:
                    for part in server_content.model_turn.parts:
                        if part.text:
                            accumulated_response += part.text
                
                if server_content and server_content.turn_complete:
                    break

        # Run send and receive concurrently
        send_task = asyncio.create_task(send_audio_loop())
        receive_task = asyncio.create_task(receive_loop())
        
        await send_task
        await receive_task

        # Parse and Print JSON
        print("\n🤖 Raw LLM Response:")
        print(accumulated_response)
        
        try:
            # Clean up markdown code blocks if present
            clean_json = accumulated_response.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_json)
            print("\n✅ Parsed JSON:")
            print(json.dumps(data, indent=2))
            
            if "feedback" in data:
                text = data["feedback"]
                print(f"🗣️ Speaking: {text}")
                try:
                    subprocess.Popen(["espeak", text], stderr=subprocess.DEVNULL)
                except FileNotFoundError:
                    pass
        except json.JSONDecodeError:
            print("⚠️ Failed to parse JSON response.")