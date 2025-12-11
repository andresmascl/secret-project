import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def run_claude(command_text):
    print("🤖 Claude Computer Use executing:", command_text)

    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=4096,
        tools=[
            {"type": "computer_vision"},
            {"type": "computer_use"}
        ],
        messages=[
            {
                "role": "user",
                "content": f"Execute this command on my computer: {command_text}"
            }
        ]
    )

    print("🔧 Claude responded:")
    print(response)