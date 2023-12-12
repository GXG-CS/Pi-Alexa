import os
import argparse

def play_audio(file_path):
    if os.path.exists(file_path):
        os.system(f"afplay '{file_path}'")
    else:
        print("Audio file not found.")

def main():
    parser = argparse.ArgumentParser(description="Audio File Player")
    parser.add_argument('--audio_file', type=str, help='Path to the audio file', required=True)
    args = parser.parse_args()

    play_audio(args.audio_file)

if __name__ == "__main__":
    main()
