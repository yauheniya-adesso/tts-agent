import os
import numpy as np

text_input_de = """Künstliche Intelligenz hat sich seit ihrer Entstehung in den 1950er Jahren rasant entwickelt, angefangen mit frühen symbolischen Denksystemen und regelbasierten Systemen.
Im Laufe der Jahrzehnte hat sich KI in Bereiche wie Computervision, Verarbeitung natürlicher Sprache und Audioverständnis erweitert und transformiert Industrien und die Gesellschaft."""

text_input_en = """Artificial Intelligence has evolved rapidly since its inception in the 1950s, starting with early symbolic reasoning and rule-based systems.
Over the decades, AI has expanded into areas like computer vision, natural language processing, and audio understanding, transforming industries and society."""

output_folder = "voice_samples"
os.makedirs(output_folder, exist_ok=True)

# ----------------------
# 1. gTTS
# ----------------------
try:
    from gtts import gTTS
    print("[gTTS] Generating audio...")
    
    # gTTS supports multiple accents for English and German
    # English accents
    en_accents = ['com.au', 'co.uk', 'us', 'co.in', 'ie', 'com.ng']
    for accent in en_accents:
        try:
            tts_gtts = gTTS(text_input_en, lang='en', tld=accent)
            voice_name = accent.replace('.', '_')
            path = os.path.join(output_folder, f"gtts_en_{voice_name}.mp3")
            tts_gtts.save(path)
            print(f"[gTTS] Done -> {path}")
        except Exception as e:
            print(f"[gTTS] Error with English accent {accent}: {e}")
    
    # German accents
    de_accents = ['de']  # Germany, Austria, Switzerland
    for accent in de_accents:
        try:
            tts_gtts = gTTS(text_input_de, lang='de', tld=accent if accent != 'de' else 'de')
            path = os.path.join(output_folder, f"gtts_de_{accent}.mp3")
            tts_gtts.save(path)
            print(f"[gTTS] Done -> {path}")
        except Exception as e:
            print(f"[gTTS] Error with German accent {accent}: {e}")
            
except Exception as e:
    print(f"[gTTS] Error: {e}")

# ----------------------
# 2. Coqui TTS
# ----------------------
try:
    from TTS.api import TTS
    print("[Coqui TTS] Generating audio...")
    
    # Define minimal set of models: one male and one female for each language
    models_to_use = {
        'en_female': 'tts_models/en/ljspeech/vits',  # Female English voice
        'en_male': 'tts_models/en/vctk/vits',  # Multi-speaker (we'll use a male voice)
        'de_female': 'tts_models/de/thorsten/vits',  # Male voice (Thorsten is male, but it's the main German model)
        'de_male': 'tts_models/de/thorsten/vits',  # Same model, will use different speaker if available
    }
    
    # English Female
    try:
        print(f"[Coqui TTS] Loading English female voice...")
        tts_en_female = TTS('tts_models/en/ljspeech/vits')
        path = os.path.join(output_folder, "coqui_en_female.wav")
        tts_en_female.tts_to_file(text=text_input_en, file_path=path)
        print(f"[Coqui TTS] Done -> {path}")
    except Exception as e:
        print(f"[Coqui TTS] Error with English female: {e}")
    
    # English Male (using VCTK multi-speaker model)
    try:
        print(f"[Coqui TTS] Loading English male voice...")
        tts_en_male = TTS('tts_models/en/vctk/vits')
        # Use a male speaker from VCTK (p226 is male)
        path = os.path.join(output_folder, "coqui_en_male.wav")
        if hasattr(tts_en_male, 'speakers') and tts_en_male.speakers:
            # Pick a male speaker (p226, p227, p232, p243, etc. are male)
            male_speaker = 'p226'  # Male speaker
            tts_en_male.tts_to_file(text=text_input_en, speaker=male_speaker, file_path=path)
        else:
            tts_en_male.tts_to_file(text=text_input_en, file_path=path)
        print(f"[Coqui TTS] Done -> {path}")
    except Exception as e:
        print(f"[Coqui TTS] Error with English male: {e}")
    
    # German - Thorsten (male voice)
    try:
        print(f"[Coqui TTS] Loading German male voice...")
        tts_de_male = TTS('tts_models/de/thorsten/vits')
        path = os.path.join(output_folder, "coqui_de_male.wav")
        tts_de_male.tts_to_file(text=text_input_de, file_path=path)
        print(f"[Coqui TTS] Done -> {path}")
    except Exception as e:
        print(f"[Coqui TTS] Error with German male: {e}")
    
    # German Female (using CSS10 if available, otherwise note it's not available)
    try:
        print(f"[Coqui TTS] Loading German female voice...")
        tts_de_female = TTS('tts_models/de/css10/vits-neon')
        path = os.path.join(output_folder, "coqui_de_female.wav")
        tts_de_female.tts_to_file(text=text_input_de, file_path=path)
        print(f"[Coqui TTS] Done -> {path}")
    except Exception as e:
        print(f"[Coqui TTS] German female voice not available or error: {e}")
        print(f"[Coqui TTS] Note: Coqui TTS has limited German female voices")
            
except Exception as e:
    print(f"[Coqui TTS] Error: {e}")

# ----------------------
# 3. Kokoro TTS
# ----------------------
try:
    from kokoro import KPipeline
    from scipy.io.wavfile import write
    print("[Kokoro TTS] Generating audio...")
    
    # Kokoro voices according to documentation
    # English voices
    en_voices = [
        'af_heart', 'af_bella', 'af_sarah', 'af_nicole',
        'am_adam', 'am_michael',
        'bf_emma', 'bf_isabella',
        'bm_george', 'bm_lewis'
    ]
    
    # Process English voices
    pipeline_en = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for voice in en_voices:
        try:
            results = pipeline_en(text_input_en, voice=voice, speed=1.0)
            
            audio_chunks = []
            sr = 24000
            for i, result in enumerate(results):
                audio_chunks.append(result.audio)
                if i == 0:
                    sr = result.sr if hasattr(result, 'sr') else 24000
            
            audio = np.concatenate(audio_chunks)
            audio_int16 = np.int16(audio * 32767)
            
            path = os.path.join(output_folder, f"kokoro_en_{voice}.wav")
            write(path, sr, audio_int16)
            print(f"[Kokoro TTS] Done -> {path}")
        except Exception as e:
            print(f"[Kokoro TTS] Error with English voice {voice}: {e}")
    
            
except Exception as e:
    print(f"[Kokoro TTS] Error: {e}")

print(f"\n[Complete] All voice samples saved to: {output_folder}")