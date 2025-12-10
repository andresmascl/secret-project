# Voice Browser Automation System

## Project Overview

A voice-controlled browser automation system for Ubuntu/Debian that allows users to control a web browser through natural language voice commands. The system uses local wake word detection for privacy, cloud-based AI for intelligence, and local execution for control.

## Core Concept

**Say a wake word → Speak your command → Watch the browser execute it**

Example: "Hey Browser, open YouTube and search for cooking tutorials"

## System Architecture

### High-Level Flow

```
[User Voice] 
    ↓
[Local Wake Word Detection] ← Always listening locally
    ↓
[Audio Capture] ← Records after wake word
    ↓
[Cloud Transcription Service] ← Converts speech to text
    ↓
[Claude API] ← Understands intent, returns structured action
    ↓
[Local Browser Executor] ← Performs the action visibly
    ↓
[Back to Listening] ← Ready for next command
```

### Design Principles

1. **Privacy First**: Only audio after wake word is sent to cloud
2. **Hybrid Architecture**: Local processing where possible, cloud for intelligence
3. **Visual Feedback**: Browser actions are visible on screen
4. **Headless Capable**: Can run without display, but default assumes screen present
5. **Self-Contained**: Single repo deployment with minimal dependencies
6. **Extensible**: Easy to add new actions and capabilities

## Technical Stack

### Local Components

- **Wake Word Detection**: Porcupine by Picovoice
  - Runs continuously with minimal CPU usage
  - Triggers audio capture on detection
  - No network required

- **Audio Capture**: PyAudio or sounddevice
  - Captures audio after wake word
  - Configurable duration or silence detection
  - Formats audio for cloud service

- **Browser Automation**: Playwright
  - Runs in headed mode (visible browser)
  - Executes parsed actions from JSON
  - Supports Chrome/Firefox/Safari

- **Service Management**: systemd
  - Runs as background service
  - Auto-starts on boot
  - Easy start/stop/restart

### Cloud Components

- **Speech-to-Text**: OpenAI Whisper API
  - Transcribes captured audio to text
  - High accuracy, multiple languages
  - Fast processing (~1-2 seconds)

- **Intent Understanding**: Anthropic Claude API
  - Receives transcript + action grid
  - Understands user intent
  - Returns structured JSON with action parameters

### Data Flow Format

**Audio → Cloud → JSON → Action**

Example JSON response from Claude:
```json
{
  "intent": "navigate_and_search",
  "confidence": 0.95,
  "parameters": {
    "site": "youtube.com",
    "search_query": "cooking tutorials"
  },
  "actions": [
    {
      "type": "navigate",
      "url": "https://youtube.com"
    },
    {
      "type": "search",
      "selector": "input[name='search_query']",
      "value": "cooking tutorials"
    },
    {
      "type": "submit",
      "selector": "button[type='submit']"
    }
  ]
}
```

## Action Grid

The **Action Grid** is a configuration file that defines what the system can do. It's sent to Claude as context to help it understand available capabilities.

### Supported Action Categories

1. **Navigation**
   - Open URLs
   - Go back/forward
   - Refresh page
   - Close tabs

2. **Search**
   - Enter text in search fields
   - Submit searches
   - Site-specific search (YouTube, Google, etc.)

3. **Interaction**
   - Click elements
   - Fill forms
   - Scroll
   - Take screenshots

4. **Content**
   - Read page content
   - Extract information
   - Summarize pages

### Action Grid Format

Located in: `config/actions.json`

```json
{
  "version": "1.0",
  "actions": {
    "navigate": {
      "description": "Navigate to a URL",
      "parameters": ["url"],
      "example": "open google.com"
    },
    "search": {
      "description": "Search on a website",
      "parameters": ["site", "query"],
      "example": "search youtube for cats"
    },
    "click": {
      "description": "Click an element",
      "parameters": ["selector", "text"],
      "example": "click the login button"
    }
  }
}
```

## Repository Structure

```
voice-browser-automation/
├── README.md                    # User-facing documentation
├── ARCHITECTURE.md              # This document
├── LICENSE                      # Project license
├── install.sh                   # One-command installation script
├── start.sh                     # Launch the assistant
├── stop.sh                      # Stop the assistant
│
├── config/
│   ├── actions.json            # Action grid definition
│   ├── settings.yaml           # Configuration (API keys, etc.)
│   └── settings.example.yaml   # Template for settings
│
├── services/
│   ├── voice-browser.service   # systemd service file
│   └── setup-service.sh        # Service installation script
│
├── src/
│   ├── main.py                 # Main orchestration loop
│   ├── wakeword_listener.py    # Wake word detection
│   ├── audio_capture.py        # Audio recording
│   ├── cloud_processor.py      # Whisper + Claude integration
│   ├── browser_executor.py     # Playwright automation
│   ├── action_parser.py        # JSON parsing and validation
│   └── utils/
│       ├── logger.py           # Logging utilities
│       └── config_loader.py    # Configuration management
│
├── tests/
│   ├── test_wakeword.py
│   ├── test_audio.py
│   ├── test_cloud.py
│   └── test_executor.py
│
├── logs/                        # Application logs (gitignored)
├── requirements.txt             # Python dependencies
└── .env.example                # Environment variables template
```

## Setup and Installation

### Prerequisites

- Ubuntu 20.04+ or Debian 11+ (64-bit)
- Python 3.8+
- Working microphone
- Display (screen assumed present)
- Internet connection
- API keys for:
  - OpenAI (Whisper API)
  - Anthropic (Claude API)
  - Picovoice (Porcupine wake word)

### Installation Steps

```bash
# Clone the repository
git clone https://github.com/yourusername/voice-browser-automation.git
cd voice-browser-automation

# Run installation script
./install.sh

# Configure API keys
cp config/settings.example.yaml config/settings.yaml
nano config/settings.yaml  # Add your API keys

# Start the service
./start.sh
```

### Configuration

Edit `config/settings.yaml`:

```yaml
wake_word:
  keyword: "hey browser"
  sensitivity: 0.5

audio:
  sample_rate: 16000
  record_duration: 5  # seconds
  silence_detection: true

api_keys:
  openai: "your-openai-key"
  anthropic: "your-anthropic-key"
  picovoice: "your-picovoice-key"

browser:
  headless: false
  browser_type: "chromium"  # chromium, firefox, webkit
  
logging:
  level: "INFO"
  file: "logs/voice-browser.log"
```

## Development Workflow

### For Humans

1. Read this document to understand the architecture
2. Check `README.md` for user instructions
3. Review `config/actions.json` to understand capabilities
4. Modify components as needed
5. Test with `pytest tests/`
6. Submit PRs with clear descriptions

### For AI Coding Assistants

When asked to work on this project:

1. **Understand the flow**: Wake word → Audio → Cloud → JSON → Browser
2. **Follow the structure**: Keep components in their designated files
3. **Respect the action grid**: All new capabilities must be added to `actions.json`
4. **Maintain JSON contract**: Browser executor expects specific JSON format from Claude
5. **Error handling**: Always wrap cloud API calls and browser actions in try-catch
6. **Logging**: Use the logger utility for all important events
7. **Testing**: Write tests for new features

### For LLMs (Like Claude)

When processing voice commands in this system:

1. You receive: `{"transcript": "user's spoken command", "action_grid": {...}}`
2. You must return valid JSON matching the schema shown above
3. Only use actions defined in the action_grid
4. Be specific with selectors (CSS or text-based)
5. Break complex commands into multiple sequential actions
6. Return confidence score (0.0-1.0)
7. If unsure, ask for clarification in the response

## Component Specifications

### 1. Wake Word Listener (`wakeword_listener.py`)

**Purpose**: Continuously listen for wake word, trigger audio capture

**Key Functions**:
- `start_listening()`: Begin monitoring audio input
- `on_wake_word_detected()`: Callback when wake word heard
- `stop_listening()`: Clean shutdown

**Performance Requirements**:
- CPU usage < 5% when idle
- Detection latency < 200ms
- False positive rate < 1%

### 2. Audio Capture (`audio_capture.py`)

**Purpose**: Record audio after wake word detection

**Key Functions**:
- `capture_audio(duration)`: Record for specified time
- `detect_silence()`: Stop recording when user stops speaking
- `save_audio(format)`: Save to temporary file for upload

**Output**: WAV or MP3 file ready for cloud upload

### 3. Cloud Processor (`cloud_processor.py`)

**Purpose**: Handle all cloud API interactions

**Key Functions**:
- `transcribe_audio(audio_file)`: Send to Whisper API
- `get_intent(transcript, action_grid)`: Send to Claude API
- `parse_response(json)`: Validate and return structured data

**Error Handling**: Retry logic, timeout handling, API error messages

### 4. Browser Executor (`browser_executor.py`)

**Purpose**: Execute browser actions from JSON commands

**Key Functions**:
- `initialize_browser()`: Start Playwright browser
- `execute_action(action_json)`: Perform single action
- `execute_sequence(actions_list)`: Perform multiple actions in order
- `take_screenshot()`: Capture visual feedback
- `close_browser()`: Clean shutdown

**Safety**: Validate all actions, sanitize inputs, respect timeouts

### 5. Main Orchestrator (`main.py`)

**Purpose**: Coordinate all components in main loop

**Main Loop**:
```python
while running:
    wait_for_wake_word()
    audio = capture_audio()
    transcript = transcribe(audio)
    action_json = get_intent(transcript)
    execute_in_browser(action_json)
    provide_feedback()
```

## Security Considerations

1. **API Keys**: Never commit to git, use environment variables
2. **Input Validation**: Sanitize all user inputs before browser execution
3. **Action Restrictions**: Limit dangerous operations (file access, system commands)
4. **Rate Limiting**: Prevent API abuse
5. **Sandboxing**: Consider running browser in isolated environment

## Performance Targets

- Wake word detection: < 200ms latency
- Audio capture: 3-5 seconds typical
- Cloud processing: 2-4 seconds total
- Browser action: 1-3 seconds per action
- Total response time: < 10 seconds for simple commands

## Future Enhancements

- [ ] Multi-language support
- [ ] Custom wake word training
- [ ] Voice feedback (TTS responses)
- [ ] Command history and recall
- [ ] Multi-tab management
- [ ] Screenshot analysis
- [ ] Macro recording
- [ ] Headless mode toggle
- [ ] Mobile device support
- [ ] Plugin system for extensions

## Testing Strategy

### Unit Tests
- Test each component independently
- Mock cloud APIs for faster testing
- Validate JSON parsing and generation

### Integration Tests
- Test full pipeline with real APIs (in CI/CD)
- Browser automation scenarios
- Error recovery paths

### Manual Testing
- Real-world voice commands
- Different accents and speech patterns
- Edge cases and error conditions

## Troubleshooting

### Common Issues

**Wake word not detecting**
- Check microphone permissions
- Adjust sensitivity in config
- Verify Porcupine API key

**Cloud API errors**
- Verify API keys are correct
- Check internet connection
- Review rate limits

**Browser actions failing**
- Check selectors are still valid
- Verify website hasn't changed
- Review Playwright logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Update documentation
6. Submit a pull request

## License

Mine

## Contact

None yet

---

**Document Version**: 1.0  
**Last Updated**: December 2025  
**Maintained By**: Andresm@
