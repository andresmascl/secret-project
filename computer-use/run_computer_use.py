import base64
import time
import io
import pyautogui
from screeninfo import get_monitors
from openai import OpenAI


client = OpenAI()


def screenshot_png_bytes():
    image = pyautogui.screenshot()
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()


def encode_png_base64(png_bytes):
    return base64.b64encode(png_bytes).decode("utf-8")


def capture_screenshot():
    png = screenshot_png_bytes()
    return encode_png_base64(png)


def system_prompt():
    return """You are a computer-control agent.

You can:
- click
- double_click
- right_click
- scroll
- press keyboard keys
- type text
- move the mouse
- take screenshots

Always think step-by-step.
"""


def main():
    print("🖥️ Computer Use agent initialized. Type a command.\n")

    while True:
        user = input("User command: ").strip()
        if not user:
            continue
        if user.lower() in ["exit", "quit"]:
            break

        screenshot_b64 = capture_screenshot()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt()},
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": user},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/png;base64,{screenshot_b64}"
                        },
                    ]
                },
            ]
        )

        print("\n🤖 Assistant:")
        print(response.choices[0].message.content)
        print("-" * 50)


if __name__ == "__main__":
    main()
