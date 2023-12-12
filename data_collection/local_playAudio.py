import argparse
import subprocess

def play_audio(file_path):
    try:
        # Use the aplay command to play the audio file
        subprocess.run(['aplay', file_path])
    except Exception as e:
        print(f"Error playing audio: {e}")

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Play a WAV file.')
    parser.add_argument('file_path', type=str, help='Path to the WAV file to play')

    # Parse the command line argument
    args = parser.parse_args()

    # Play the audio
    play_audio(args.file_path)
