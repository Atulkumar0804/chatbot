# Voice-Enabled AI Chatbot

A complete voice-enabled chatbot using Google Gemini LLM with speech recognition and text-to-speech capabilities.

## ✨ Features

- 🎤 **Voice Input**: Speech-to-text using Google Speech Recognition
- 🔊 **Voice Output**: Text-to-speech responses 
- 🧠 **Smart AI**: Powered by Google Gemini 1.5 Flash
- 🔍 **Web Search**: Real-time information retrieval for current events
- 💬 **Text Input**: Always available as fallback
- 🎯 **Smart Routing**: Automatically detects when to search for current information

## 📁 Project Structure

```
chatbot/
├── .env                                    # Environment variables (API keys) - DO NOT COMMIT
├── .env.example                           # Environment template file
├── .gitignore                             # Git ignore file (protects .env)
├── .venv/                                 # Python virtual environment
├── README.md                              # This file
├── complete_voice_chatbot.py              # Main chatbot (virtual environment)
├── complete_voice_chatbot_conda.py       # Conda version with enhanced audio
└── complete_voice_chatbot_system.py      # System Python version
```

## 🚀 Quick Start

### Prerequisites

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd chatbot
```

2. **Set up environment variables:**
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your actual API keys
nano .env  # or use your preferred editor
```

3. **API Keys Required:**
   - **Google AI API key** (for Gemini) - Get from: https://aistudio.google.com/app/apikey
   - **Serper API key** (for web search) - Get from: https://serper.dev/ (optional)

### Installation & Usage

**Option 1: Conda Version (Recommended for voice)**
```bash
# Install dependencies
conda install -c conda-forge pyaudio
python -m pip install speechrecognition pyttsx3

# Run the chatbot
python complete_voice_chatbot_conda.py

# For single questions:
python complete_voice_chatbot_conda.py "What is artificial intelligence?"
```

**Option 2: Virtual Environment Version**
```bash
# Activate virtual environment
source .venv/bin/activate

# Run the chatbot
python complete_voice_chatbot.py
```

**Option 3: System Python Version**
```bash
# Install system dependencies
sudo apt install python3-pyaudio portaudio19-dev
pip3 install --user speechrecognition pyttsx3 langchain-google-genai

# Run the chatbot
/usr/bin/python3 complete_voice_chatbot_system.py
```

## 🎤 Using Voice Features

### Interactive Mode:
1. Run the chatbot: `python complete_voice_chatbot_conda.py`
2. Type your questions normally for text input
3. Type `voice` to switch to voice input
4. Speak clearly when prompted
5. Type `quit` to exit

### Voice Commands:
- **"voice"** - Switch to voice input mode
- **"quit"/"exit"** - Exit the chatbot
- **Ask any question** - The bot will respond with both text and speech

## 🔧 Troubleshooting

### Microphone Issues:
- Make sure microphone is connected and working
- Try the conda version: `python complete_voice_chatbot_conda.py`
- The chatbot automatically tests multiple audio devices

### Missing Dependencies:
```bash
# For conda environment:
conda install -c conda-forge pyaudio
python -m pip install speechrecognition pyttsx3

# For system Python:
sudo apt install python3-pyaudio
pip3 install --user speechrecognition pyttsx3
```

### API Issues:
- Verify your `.env` file has valid API keys
- Check internet connection
- Ensure Google AI API key has proper permissions

## 💡 Features Breakdown

**Voice Recognition:**
- Uses Google Speech Recognition API
- Automatic microphone device detection
- Noise adjustment and calibration
- Fallback to text input if voice fails

**Text-to-Speech:**
- Uses pyttsx3 library
- Adjustable speech rate and volume
- Cross-platform compatibility

**Smart Search:**
- Automatically detects questions needing current information
- Keywords: "latest", "current", "today", "news", "cricket", etc.
- Uses Serper API for web search
- Combines knowledge base with real-time data

**AI Responses:**
- Google Gemini 1.5 Flash model
- Conversational and concise responses
- Context-aware conversations
- Optimized for voice interaction

## 🎯 Example Usage

```bash
# Start interactive mode
python complete_voice_chatbot_conda.py

# Example conversation:
💬 You: What is machine learning?
🔊 Bot: [Speaks explanation of machine learning]

💬 You: voice
🎤 Listening... (speak now)
📝 You said: What are today's cricket scores?
🔊 Bot: [Searches web and speaks current cricket scores]

💬 You: quit
👋 Goodbye!
```

## 🔄 Version Differences

- **complete_voice_chatbot_conda.py**: Best for voice features, handles audio device conflicts
- **complete_voice_chatbot.py**: Virtual environment version, reliable text + TTS
- **complete_voice_chatbot_system.py**: System Python version, minimal conflicts

## 📝 Notes

- The chatbot automatically chooses between knowledge base and web search
- Voice output works even if voice input is unavailable
- All versions support text input as a reliable fallback
- Conda version has the best microphone support and device detection
