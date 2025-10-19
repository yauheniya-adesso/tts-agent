import fitz 
import os
import time
from typing import Tuple
import sys
from itertools import cycle
import threading
from datetime import datetime

# TTS Engine selection
TTS_ENGINE = "kokoro"  # Options: "kokoro" or "coqui"
TTS_LANGUAGE = "en"   # Options: "en" (English) or "de" (German)

if TTS_ENGINE.lower() == "kokoro":
    from models.kokoro_tts_offline import KokoroTTS
    TTSClass = KokoroTTS
elif TTS_ENGINE.lower() == "coqui":
    from models.coqui_tts_offline import CoquiTTS
    TTSClass = CoquiTTS
else:
    raise ValueError(f"Unknown TTS engine: {TTS_ENGINE}. Use 'kokoro' or 'coqui'")


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract and combine text from all PDF pages"""
    with fitz.open(pdf_path) as doc:
        return "\n".join([page.get_text() for page in doc])

def save_text_to_file(text: str, filename: str):
    """Save text content to a file with UTF-8 encoding"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

def load_text_from_file(filename: str) -> str:
    """Load text content from a file"""
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

def calculate_text_metrics(text: str) -> Tuple[int, int, int]:
    """Calculate character, word, and approximate token counts"""
    return (
        len(text),  # Characters
        len(text.split()),  # Words
        int(len(text) / 4)  # Approximate tokens (1 token ≈ 4 chars)
    )

def clean_text_for_tts(text: str) -> str:
    """Normalize text while preserving paragraph structure"""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    cleaned_paragraphs = []
    for p in paragraphs:
        p = p.replace("\n", " ")
        p = " ".join(p.split())  # Collapse multiple spaces
        cleaned_paragraphs.append(p)
    return "\n\n".join(cleaned_paragraphs)

def text_to_speech(text: str, output_path: str, tts_engine, 
                   voice: str = "default", speed: float = 1.0):
    """Convert text to audio using selected TTS engine"""
    tts_engine.generate_audio(text, output_path, voice=voice, speed=speed)

def format_processing_time(seconds: float) -> str:
    """Convert seconds to MM:SS format"""
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes):02d}:{int(seconds):02d}"

def generate_conversion_report(raw_metrics: Tuple[int, int, int],
                            clean_metrics: Tuple[int, int, int],
                            output_path: str,
                            processing_time: float,
                            engine_name: str):
    """Generate formatted conversion metrics report"""
    print("\n" + "="*50)
    print(f"PDF to WAV Conversion Complete ({engine_name})")
    print("="*50)
    print(f"\nAudio file saved to: {output_path}")
    print(f"Processing time: {format_processing_time(processing_time)} (MM:SS)")
    
    print("\nText Statistics:")
    print("-"*40)
    print(f"{'Metric':<15} | {'Raw Text':>12} | {'Cleaned Text':>12}")
    print("-"*40)
    print(f"{'Characters':<15} | {raw_metrics[0]:>12,} | {clean_metrics[0]:>12,}")
    print(f"{'Words':<15} | {raw_metrics[1]:>12,} | {clean_metrics[1]:>12,}")
    print(f"{'Tokens (approx)':<15} | {raw_metrics[2]:>12,} | {clean_metrics[2]:>12,}")
    
    print("\nOutput Files:")
    print(f"- Raw text: full_text.txt")
    print(f"- Cleaned text: cleaned_text.txt")
    print("="*50 + "\n")

def show_progress(message, stop_event):
    frames = cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    while not stop_event.is_set():
        sys.stdout.write(f'\r{message} {next(frames)}')
        sys.stdout.flush()
        time.sleep(0.2)
    sys.stdout.write('\r' + ' ' * (len(message) + 2) + '\r') 

def pdf_to_audio(pdf_path: str, output_audio: str, voice: str = "default", speed: float = 1.0):
    """Full PDF to audio conversion pipeline with selectable TTS and visual feedback"""
    start_time = time.time()
    os.makedirs(os.path.dirname(output_audio), exist_ok=True)
    
    # Initialize TTS Engine
    print(f"\n🔧 Initializing {TTS_ENGINE.upper()} TTS...")
    if TTS_ENGINE.lower() == "kokoro":
        tts_engine = TTSClass()
    else:  # coqui
        tts_engine = TTSClass(language=TTS_LANGUAGE)
    print(f"✓ {TTS_ENGINE.upper()} TTS ready\n")
    
    # Stage 1: Extract and save raw text
    print("🔍 Extracting text from PDF...")
    full_text = extract_text_from_pdf(pdf_path)
    save_text_to_file(full_text, "./temp/full_text.txt")
    
    # Manual intervention point for raw text
    print("\n📝 Raw text saved to './temp/full_text.txt'")
    input("✏️  Make your edits, then press Enter to continue...")
    full_text = load_text_from_file("./temp/full_text.txt")
    print("✓ Raw text changes applied\n")
    
    # Stage 2: Clean and save normalized text
    print("🧹 Cleaning text for TTS...")
    cleaned_text = clean_text_for_tts(full_text)
    save_text_to_file(cleaned_text, "./temp/cleaned_text.txt")
    
    # Manual intervention point for cleaned text
    print("\n📝 Cleaned text saved to './temp/cleaned_text.txt'")
    input("✏️  Make your edits, then press Enter to continue...")
    cleaned_text = load_text_from_file("./temp/cleaned_text.txt")
    print("✓ Cleaned text changes applied\n")
    
    # Estimate time before actual TTS
    raw_metrics = calculate_text_metrics(full_text)
    clean_metrics = calculate_text_metrics(cleaned_text)
    estimated_tts_seconds = int(clean_metrics[0] * 0.014)  # Based on character count

    print("Text Statistics:")
    print("-"*60)
    print(f"{'Metric':<15} | {'Raw Text':>12} | {'Cleaned Text':>12}")
    print("-"*60)
    print(f"{'Characters':<15} | {raw_metrics[0]:>12,} | {clean_metrics[0]:>12,}")
    print(f"{'Words':<15} | {raw_metrics[1]:>12,} | {clean_metrics[1]:>12,}")
    print(f"{'Tokens (approx)':<15} | {raw_metrics[2]:>12,} | {clean_metrics[2]:>12,}")
    print(f"\nApproximate processing time: {format_processing_time(estimated_tts_seconds)} (MM:SS)\n")

    # Stage 3: Generate audio with visual feedback
    now = datetime.now()
    print(f"Current time: {now.strftime('%d.%m.%Y %H:%M')}")
    print(f"🔊 Converting text to speech ({TTS_ENGINE.upper()}, voice: {voice}, speed: {speed}x):")
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=show_progress, args=("Generating audio", stop_event))
    spinner_thread.start()
    try:
        text_to_speech(cleaned_text, output_audio, tts_engine, voice=voice, speed=speed)
    finally:
        stop_event.set()
        spinner_thread.join()
    print("✓ Audio generation complete\n")
    
    # Generate final report
    generate_conversion_report(
        raw_metrics=calculate_text_metrics(full_text),
        clean_metrics=calculate_text_metrics(cleaned_text),
        output_path=output_audio,
        processing_time=time.time() - start_time,
        engine_name=TTS_ENGINE.upper()
    )

FOLDER = "pdf"
STUDY = "2024_Zheng+"

# Usage
if __name__ == "__main__":
    # Configuration
    # TTS_ENGINE = "coqui"  # Change to "kokoro" or "coqui"
    # TTS_LANGUAGE = "en"   # Options: "en" (English) or "de" (German)
    
    pdf_to_audio(
        f"./{FOLDER}/{STUDY}.pdf",
        f"./audio/{STUDY}.wav",
        voice="bf_emma",  # Coqui: "default", Kokoro: "af_heart", "am_adam", "bf_emma", "bm_george"
        speed=1.0
    )