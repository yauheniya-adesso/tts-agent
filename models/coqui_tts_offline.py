# -*- coding: utf-8 -*-
# Coqui TTS Offline Usage
import os
import sys

try:
    from TTS.api import TTS
except ImportError:
    print("❌ Coqui TTS not installed. Install with: pip install TTS")
    sys.exit(1)


class CoquiTTS:
    """Wrapper class for Coqui TTS with offline support"""
    
    # Available models: language code -> model path
    MODELS = {
        "de": "tts_models/de/thorsten/vits",      # German
        "en": "tts_models/en/ljspeech/vits",      # English
    }
    
    # Available voices per language
    VOICES = {
        "de": ["default"],  # German model (Thorsten has one default voice)
        "en": ["default"],  # English model (Glow-TTS has one default voice)
    }
    
    def __init__(self, language: str = "en", gpu: bool = False):
        """
        Initialize Coqui TTS
        
        Args:
            language: Language code ("en" for English, "de" for German)
            gpu: Use GPU if available (default: False for CPU)
        """
        if language not in self.MODELS:
            raise ValueError(
                f"Unsupported language: {language}. "
                f"Available: {', '.join(self.MODELS.keys())}"
            )
        
        self.language = language
        self.gpu = gpu
        self.model_path = self.MODELS[language]
        self.tts = None
        self._initialize_pipeline()
    
    def _initialize_pipeline(self):
        """Initialize Coqui TTS pipeline"""
        try:
            print(f"🔧 Loading Coqui TTS model for {self.language.upper()}...")
            self.tts = TTS(
                model_name=self.model_path,
                gpu=self.gpu
            )
            print(f"✓ Coqui TTS model loaded")
        except Exception as e:
            print(f"❌ Failed to initialize Coqui TTS: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    def generate_audio(self, text: str, output_path: str, voice: str = "default", speed: float = 1.0):
        """
        Generate audio from text and save to file
        
        Args:
            text: Text to convert to speech
            output_path: Path to save the output audio file (WAV format)
            voice: Voice to use (currently only "default" supported per language)
            speed: Speech speed multiplier (not directly supported by Coqui, used for compatibility)
        """
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            
            # Generate and save audio
            self.tts.tts_to_file(
                text=text,
                file_path=output_path
            )
            
            print(f"✓ Audio saved to {output_path}")
            
        except Exception as e:
            print(f"❌ Error generating audio: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    @staticmethod
    def list_available_models():
        """Return dictionary of available models"""
        return CoquiTTS.MODELS
    
    @staticmethod
    def list_available_voices(language: str = "en"):
        """Return list of available voices for a language"""
        if language not in CoquiTTS.VOICES:
            return []
        return CoquiTTS.VOICES[language]