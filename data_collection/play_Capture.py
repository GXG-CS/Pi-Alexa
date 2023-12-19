import argparse
import subprocess
import threading
import time

def play_audio(file_path):
    try:
        # Use the aplay command to play the audio file
        subprocess.run(['aplay', file_path])
    except Exception as e:
        print(f"Error playing audio: {e}")

def capture_traffic(output_file, duration):
    try:
        # Use tcpdump to capture traffic on wlan0 for a specified duration, saving to the output file
        subprocess.run(['sudo', 'tcpdump', '-i', 'wlan0', '-w', output_file, '-G', str(duration), '-W', '1'])
    except Exception as e:
        print(f"Error capturing traffic: {e}")


if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Play a WAV file and capture traffic.')
    parser.add_argument('file_path', type=str, help='Path to the WAV file to play')
    parser.add_argument('output_file', type=str, help='Path to save the traffic capture file')
    parser.add_argument('--duration', type=int, default=30, help='Duration to capture traffic (in seconds)')

    # Parse the command line arguments
    args = parser.parse_args()

    # Start traffic capture in a separate thread
    capture_thread = threading.Thread(target=capture_traffic, args=(args.output_file, args.duration))
    capture_thread.start()

    # Delay to ensure traffic capture starts before playing audio
    time.sleep(2)

    # Play the audio
    play_audio(args.file_path)

    # Wait for the capture thread to finish
    capture_thread.join()

# python play_Capture.py audio_A/2_audio.wav traffic_W/test2.pcap --duration 20