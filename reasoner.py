import asyncio
import os
from google import genai
from google.genai import types
from config import PROJECT_ID, REGION, MODEL_NAME

# Initialize the new GenAI client
client = genai.Client(vertexai=True, project=PROJECT_ID, location=REGION)

# Define your "Intents" as Tools
tools = [
    {
        "function_declarations": [
            {
                "name": "move_robot",
                "description": "Moves the robot in a specific direction for a distance",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "direction": {"type": "STRING", "enum": ["forward", "back", "left", "right"]},
                        "distance": {"type": "NUMBER", "description": "Distance in meters"}
                    },
                    "required": ["direction", "distance"]
                }
            },
            # Add more intents here as FunctionDeclarations
        ]
    }
]

async def run_live_session(audio_generator):
    """
    Manages the real-time interaction loop.
    """
    config = types.LiveConnectConfig(
        model=MODEL_NAME,
        system_instruction="You are Scrapbot. Use the provided tools to help the user. If info is missing, ask.",
        tools=tools,
        generation_config={"speech_config": {"voice_config": {"prebuilt_voice_config": {"voice_name": "Aoede"}}}}
    )

    async with client.aio.models.live.connect(model=MODEL_NAME, config=config) as session:
        # Task 1: Send Audio
        async def send_audio():
            async for chunk in audio_generator:
                if chunk == "START_SESSION": continue # Metadata chunk
                await session.send(input=chunk, end_of_turn=False)

        # Task 2: Receive and Process Events
        async def receive_events():
            async for message in session.receive():
                # Handle Tool Calls (Intents)
                if message.tool_call:
                    for call in message.tool_call.function_calls:
                        print(f"🎯 INTENT DETECTED: {call.name} with {call.args}")
                        # Return tool response to "forget" the turn or fulfill it
                        await session.send(
                            types.LiveClientToolResponse(
                                function_responses=[{"name": call.name, "response": {"status": "success"}}]
                            )
                        )
                        return # Closing session after tool execution to 'forget' context

                # Handle model's spoken response
                if message.server_content and message.server_content.model_turn:
                    # You could pipe this to local speakers here
                    pass

        # Run both concurrently
        await asyncio.gather(send_audio(), receive_events())