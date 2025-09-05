#!/usr/bin/env python3
"""
Complete Voice Chatbot with Speech Recognition and Text-to-Speech
Handles both voice input and text input, with intelligent search
"""

import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv

# Voice libraries (optional)
VOICE_INPUT_AVAILABLE = False
TTS_AVAILABLE = False

try:
    import speech_recognition as sr
    import pyaudio  # Test if PyAudio is working
    VOICE_INPUT_AVAILABLE = True
except ImportError:
    pass

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    pass

# LangChain for LLM
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
import requests

load_dotenv()

class CompleteVoiceChatbot:
    def __init__(self):
        """Initialize the complete voice chatbot"""
        
        # Initialize speech recognition if available
        self.voice_input = VOICE_INPUT_AVAILABLE
        if self.voice_input:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                print("🎤 Speech recognition enabled")
                
                # Test microphone
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    
            except Exception as e:
                print(f"⚠️ Microphone error: {e}")
                self.voice_input = False
        
        # Initialize text-to-speech if available
        self.tts = TTS_AVAILABLE
        if self.tts:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 150)
                self.tts_engine.setProperty('volume', 0.9)
                print("🔊 Text-to-speech enabled")
            except Exception as e:
                print(f"⚠️ TTS error: {e}")
                self.tts = False
        
        # Status report
        if not self.voice_input and not self.tts:
            print("📱 Running in text-only mode")
        elif not self.voice_input:
            print("📱 Text input + speech output mode")
        elif not self.tts:
            print("🎤 Voice input + text output mode")
        else:
            print("🎤🔊 Full voice interaction mode")
        
        # Initialize Gemini
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file")
        
        self.chatbot = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            google_api_key=self.api_key,
        )
        
        print("🤖 Complete Voice Chatbot ready!")
    
    def speak(self, text):
        """Convert text to speech or display it"""
        print(f"🔊 Bot: {text}")
        
        if self.tts:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"⚠️ Speech error: {e}")
    
    def listen(self):
        """Listen for speech input"""
        if not self.voice_input:
            return None
            
        try:
            print("\n🎤 Listening... (speak now or press Ctrl+C for text input)")
            
            with self.microphone as source:
                # Listen for speech
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=10)
            
            print("🔄 Converting speech to text...")
            text = self.recognizer.recognize_google(audio)
            print(f"📝 You said: {text}")
            return text.strip()
            
        except sr.WaitTimeoutError:
            print("⏰ No speech detected")
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand speech")
            return None
        except Exception as e:
            print(f"❌ Speech recognition error: {e}")
            return None
    
    def get_text_input(self):
        """Get text input from user"""
        return input("💬 Type your message: ").strip()
    
    def get_input(self, prefer_voice=True):
        """Get input from user (voice or text)"""
        if prefer_voice and self.voice_input:
            speech_input = self.listen()
            if speech_input:
                return speech_input
            
            # Fallback to text if speech failed
            print("🔄 Switching to text input...")
        
        return self.get_text_input()
    
    def search_web(self, query):
        """Search web for current information"""
        try:
            serper_key = os.getenv("SERPER_API_KEY")
            if not serper_key:
                return None
            
            url = "https://google.serper.dev/search"
            headers = {'X-API-KEY': serper_key, 'Content-Type': 'application/json'}
            payload = {"q": query, "num": 3}
            
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            data = response.json()
            
            results = []
            
            if 'knowledgeGraph' in data:
                kg = data['knowledgeGraph']
                if 'description' in kg:
                    results.append(kg['description'])
            
            if 'organic' in data:
                for result in data['organic'][:2]:
                    snippet = result.get('snippet', '')
                    if snippet:
                        results.append(snippet)
            
            return " ".join(results) if results else None
            
        except Exception as e:
            print(f"🔍 Search error: {e}")
            return None
    
    def needs_search(self, text):
        """Check if question needs web search"""
        search_indicators = [
            'latest', 'recent', 'current', 'today', 'news', 'upcoming', 'future',
            'cricket', 'match', 'schedule', 'tariff', 'search', 'when', 'dates',
            'world cup', 'asia cup', 'olympics', 'election', 'weather', 'stock'
        ]
        return any(indicator in text.lower() for indicator in search_indicators)
    
    def get_response(self, question):
        """Get response with optional web search"""
        try:
            web_info = None
            if self.needs_search(question):
                print("🔍 Searching for current information...")
                web_info = self.search_web(question)
            
            if web_info:
                prompt = f"""Question: {question}

Current information: {web_info}

Provide a conversational response (50-80 words) suitable for voice interaction."""
            else:
                prompt = f"""Question: {question}

Provide a conversational response (50-80 words) suitable for voice interaction."""
            
            messages = [
                SystemMessage(content=f"You are a helpful voice assistant. Today is {datetime.now().strftime('%B %d, %Y')}. Keep responses concise and conversational."),
                HumanMessage(content=prompt)
            ]
            
            response = self.chatbot.invoke(messages)
            return response.content
            
        except Exception as e:
            return f"Sorry, I had an error: {str(e)}"
    
    def run_interactive(self):
        """Run interactive voice/text chatbot"""
        print("\n🎤 Complete Voice Chatbot - Interactive Mode")
        print("="*50)
        
        if self.voice_input:
            print("🎤 Voice input available - you can speak")
        
        print("💬 Text input always available - just type your questions")
            
        if self.tts:
            print("🔊 Speech output enabled - bot will speak responses")
        else:
            print("📱 Text output mode")
            
        print("📝 Type 'quit' to exit")
        print("📝 Type 'voice' to try voice input (if available)")
        print("-" * 50)
        
        self.speak("Hello! I'm your AI assistant. What would you like to know?")
        
        while True:
            try:
                # Always default to text input for reliability
                print("\n💬 You: ", end="", flush=True)
                user_input = input().strip()
                
                if not user_input:
                    print("⚠️ Please enter a question or type 'quit' to exit")
                    continue
                
                # Check for special commands
                if user_input.lower() in ['quit', 'exit', 'stop', 'goodbye', 'bye']:
                    self.speak("Goodbye! Have a great day!")
                    print("👋 Goodbye!")
                    break
                
                # Check for voice command
                if user_input.lower() == 'voice':
                    if self.voice_input:
                        print("🎤 Switching to voice input - speak now...")
                        voice_input = self.listen()
                        if voice_input:
                            user_input = voice_input
                            print(f"🎤 Voice input received: {voice_input}")
                        else:
                            print("❌ Voice input failed, please type your question")
                            continue
                    else:
                        print("❌ Voice input not available (microphone/PyAudio issues)")
                        print("💬 Please type your question instead:")
                        continue
                
                # Process the question
                print("🤖 Processing your question...")
                response = self.get_response(user_input)
                
                # Speak and display response
                print(f"\n🔊 Bot: {response}")
                if self.tts:
                    try:
                        self.tts_engine.say(response)
                        self.tts_engine.runAndWait()
                    except Exception as e:
                        print(f"⚠️ Speech output failed: {e}")
                
                print("-" * 50)
                
            except KeyboardInterrupt:
                self.speak("Goodbye!")
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Please try again or type 'quit' to exit")
    
    def run_single_command(self, command):
        """Process single command"""
        print(f"🎤 Processing: {command}")
        print("🤖 Getting response...")
        response = self.get_response(command)
        
        # Display response
        print(f"\n🔊 Bot: {response}")
        
        # Speak response if TTS is available
        if self.tts:
            try:
                self.tts_engine.say(response)
                self.tts_engine.runAndWait()
                print("🎵 Response spoken successfully!")
            except Exception as e:
                print(f"⚠️ Speech output failed: {e}")
        
        return response

def main():
    """Main function"""
    print("🚀 Initializing Complete Voice Chatbot...")
    
    try:
        bot = CompleteVoiceChatbot()
        
        if len(sys.argv) > 1:
            # Single command mode
            command = " ".join(sys.argv[1:])
            bot.run_single_command(command)
        else:
            # Interactive mode
            bot.run_interactive()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure you have:")
        print("  - GOOGLE_API_KEY in .env file")
        print("  - Internet connection")
        print("  - Microphone (optional)")

if __name__ == "__main__":
    main()
