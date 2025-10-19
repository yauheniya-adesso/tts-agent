# -*- coding: utf-8 -*-
# Kokoro TTS Offline Usage
import os
import sys
import numpy as np
from scipy.io.wavfile import write

# Set offline mode BEFORE any imports
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['HF_DATASETS_OFFLINE'] = '1'

from kokoro import KPipeline


class KokoroTTS:
    """Wrapper class for Kokoro TTS with offline support"""
    
    def __init__(self):
        """Initialize Kokoro TTS"""
        self.sr = 24000
        self.pipeline = None
        self._verify_cache()
        self._initialize_pipeline()
    
    def _verify_cache(self):
        """Verify that required model files are cached locally"""
        cache_dir = os.path.expanduser("~/.cache/huggingface/hub")
        kokoro_model = os.path.join(cache_dir, "models--hexgrad--Kokoro-82M")
        
        if not os.path.exists(kokoro_model):
            print("\nError: Kokoro model not found in local cache.")
            print(f"Expected location: {kokoro_model}")
            print("\nTo download the model while online, run:")
            print("python -c \"")
            print("import os")
            print("os.environ.pop('HF_HUB_OFFLINE', None)")
            print("from kokoro import KPipeline")
            print("pipeline = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M')")
            print("for voice in ['af_heart', 'am_adam', 'bf_emma', 'bm_george']:")
            print("    print(f'Downloading {voice}...')")
            print("    pipeline(f'Test for {voice}', voice=voice)")
            print("print('Done!')")
            print("\"")
            sys.exit(1)
        
        print("Kokoro model found in local cache")
    
    def _initialize_pipeline(self):
        """Initialize Kokoro pipeline in offline mode"""
        try:
            print("Initializing Kokoro TTS (offline mode)...")
            self.pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
            print("Kokoro TTS ready (running fully offline)")
        except Exception as e:
            print(f"Failed to initialize Kokoro pipeline: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    def generate_audio(self, text: str, output_path: str, voice: str = "af_heart", speed: float = 1.0):
        """
        Generate audio from text and save to file
        
        Args:
            text: Text to convert to speech
            output_path: Path to save the output audio file (WAV format)
            voice: Voice to use (default: "af_heart")
            speed: Speech speed multiplier (default: 1.0)
        """
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            
            # Generate audio
            results = self.pipeline(text, voice=voice, speed=speed)
            
            # Collect and concatenate audio chunks
            audio_chunks = []
            for i, result in enumerate(results):
                audio_chunks.append(result.audio)
                if i == 0:
                    self.sr = result.sr if hasattr(result, 'sr') else 24000
            
            # Concatenate all chunks
            audio = np.concatenate(audio_chunks)
            
            # Convert to int16 for WAV file
            audio_int16 = np.int16(audio * 32767)
            
            # Save to file
            write(output_path, self.sr, audio_int16)
            print(f"Audio saved to {output_path}")
            
        except Exception as e:
            print(f"Error generating audio: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    @staticmethod
    def list_available_voices():
        """Return list of available voices"""
        return [
            "af_heart",      # Female voice
            "am_adam",       # Male voice
            "bf_emma",       # Female voice
            "bm_george",     # Male voice
        ]