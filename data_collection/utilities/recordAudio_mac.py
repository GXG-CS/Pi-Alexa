import sounddevice as sd
import wavio
import argparse

def record_audio(filename, duration=5, fs=44100, channels=1):
    print("Recording...")

    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()  # Wait until recording is finished

    wavio.write(filename, audio_data, fs, sampwidth=2)

    print(f"Recording finished, file saved as {filename}")

def main():
    parser = argparse.ArgumentParser(description="Record audio and save as WAV file.")
    parser.add_argument('output_file', type=str, help="Output WAV file name.")
    args = parser.parse_args()

    record_audio(args.output_file)

if __name__ == "__main__":
    main()
