# TTS Agent - PDF to Audio Conversion

Convert PDF documents to high-quality audio files using offline text-to-speech engines.

## Features

- Extract text from PDF files
- Manual text editing before conversion
- Support for two TTS engines (Coqui, Kokoro)
- Offline processing for privacy
- Multilingual support (English, German)

## TTS Engine Comparison

| Model | Offline | English | German |
|---------|---------|---------|--------|
| gTTS | ✘ | ✔ | ✔ |
| Coqui TTS | ✔ | ✔ | ✔ |
| Kokoro TTS | ✔ | ✔ | ✘ |

## Supported Models

### Coqui TTS

- German: `tts_models/de/thorsten/tacotron2-DDC` (Thorsten voice - Male)
- English: `tts_models/en/glow-tts/glow-tts-ljspeech` (LJSpeech voice - Female)

### Kokoro TTS

- Voices: `af_heart`, `am_adam`, `bf_emma`, `bm_george`
- Language: Automatically handles multiple languages (German is not supported)

## Installation

```bash
pip install -r requirements.txt
```

## Project Structure

```
tts-agent/
├── main.py                          # Main entry point and conversion pipeline
├── models/                          # TTS engine wrappers
│   ├── __init__.py                     # Package initialization
│   ├── kokoro_tts_offline.py           # Kokoro TTS implementation
│   └── coqui_tts_offline.py            # Coqui TTS implementation
├── scripts/                         # Model and voice comparison
├── voice_samples/                   # Compare voice samples
├── pdf/                             # Input PDF files
│   └── 2005_Buchanan.pdf               # Example PDF
├── audio/                           # Output audio files (auto-created)
├── temp/                            # Temporary text files for editing (auto-created)
└── requirements.txt                 # Python dependencies
```

## Configuration

Edit the top of `main.py` to select your TTS engine:

```python
TTS_ENGINE = "coqui"    # Options: "kokoro" or "coqui"
TTS_LANGUAGE = "en"     # Options: "en" (English) or "de" (German)
```

## Usage

```bash
python main.py
```

The script will:

1. Extract text from the PDF
2. Save raw text to `./temp/full_text.txt` (you can edit this)
3. Clean and normalize the text
4. Save cleaned text to `./temp/cleaned_text.txt` (you can edit this)
5. Generate audio and save to `./audio/2005_Buchanan.wav`
6. Display conversion statistics

## Configuration Examples

Use Coqui with German:

```python
TTS_ENGINE = "coqui"
TTS_LANGUAGE = "de"
```

Use Kokoro with English:

```python
TTS_ENGINE = "kokoro"
TTS_LANGUAGE = "en"
```

Use Coqui with English:

```python
TTS_ENGINE = "coqui"
TTS_LANGUAGE = "en"
```

## Notes

- Selected Coqui and Kokoro for superior audio quality and offline processing
- All processing happens locally with no external API calls
- Audio output is in WAV format
- Processing time depends on text length and your system hardware

## Contributing

Contributions and improvements are welcome!  

All code in this project is free to copy, modify, and reuse in your own work.


## Todo List

- [x] Try and compare different TTS models
- [x] Select TTS modes with support for offline, English, and German
- [ ] Create short voice samples for each available voice
- [ ] Voice cloning functionality (train custom voices)
- [ ] Intelligent PDF processing to remove journal artifacts (page numbers, headers, footers)
- [ ] Intelligent PDF processing to see the page instead of reading it (for complex pdfs)
- [ ] Audio file chunking for large documents
- [ ] Metadata extraction from PDFs (title, author, date)
- [ ] Support for different output formats (MP3, AAC, OGG)
- [ ] Batch processing multiple PDFs
- [ ] Audio quality settings (speed, pitch, volume normalization)
- [ ] Web interface for easier PDF uploads
- [ ] Performance optimization for faster processing
- [ ] Support for additional languages