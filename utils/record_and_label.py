# record_and_label.py
import sounddevice as sd
import soundfile as sf
import os
from pathlib import Path

OUTDIR = Path("wavs")
OUTDIR.mkdir(exist_ok=True)
METADATA = Path("metadata.csv")

samplerate = 22050  # or 44100
channels = 1
subtype = 'PCM_16'

def record_seconds(seconds):
    print(f"Recording for {seconds} seconds...")
    data = sd.rec(int(seconds * samplerate), samplerate=samplerate, channels=channels)
    sd.wait()
    return data

def interactive():
    idx = 1
    # find next index
    existing = sorted(OUTDIR.glob("*.wav"))
    if existing:
        last = existing[-1].stem
        try:
            idx = int(last) + 1
        except:
            pass

    print("Interactive recorder. Press Enter to start/stop recording of a single clip.")
    print("Type 'q' at the transcript prompt to quit.")

    while True:
        input("Press Enter to start recording. Speak after the beep...")
        # optional beep
        print(">>> RECORDING — speak now. Stop after silence or press Ctrl+C to stop.")
        # We'll record until the user presses Enter again (simpler: record fixed length; here we'll do 20s max)
        seconds = input("Enter max seconds for this clip (default 20): ").strip()
        seconds = int(seconds) if seconds.isdigit() else 20
        data = record_seconds(seconds)
        fname = OUTDIR / f"{idx:04d}.wav"
        sf.write(str(fname), data, samplerate, subtype=subtype)
        print(f"Saved {fname}")

        transcript = input("Type transcript for this file (or 'r' to re-record, 'q' to quit): ").strip()
        if transcript.lower() == 'r':
            fname.unlink()
            print("Re-recording...")
            continue
        if transcript.lower() == 'q':
            print("Quitting.")
            break

        # append to metadata file in Coqui/LJSpeech style: filename|transcript
        line = f"{fname.name}|{transcript}\n"
        with open(METADATA, "a", encoding="utf-8") as f:
            f.write(line)
        print("Transcript saved.")
        idx += 1

if __name__ == "__main__":
    interactive()
