## What Scrapbot.ai Does

- Continuously listens to microphone input
- Detects a custom wake word ("hey Mycroft")


## TODO:
1. After Wake Word Detection, Local Agent Sends PROMPT.md to LLM & Streams Speech Until it Stops.  We will use Multimodal Live API, for this, which is already enabled on GCP's Service Account. Local Agent reads and prints out the full json response from LLM for now to test LLM funcionality.
2. Replies to the user using local text-to-speech (TTS)
3. Browser automation
4. Custom Scrapbot.ai wakeword
5. Add extra wake-word filter at cloud level
6. Mobile app to serve over LAN
