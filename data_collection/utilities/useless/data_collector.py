import argparse
import subprocess
import threading
import os
import time

def play_audio(file_path):
    # Run local_playAudio.py to play the audio file
    subprocess.run(['python', 'local_playAudio.py', file_path])

def capture_traffic(duration, output_file):
    # Capture traffic with tcpdump
    subprocess.run(['sudo', 'tcpdump', '-w', output_file, '-G', str(duration), '-W', '1'])

def main(folder_path, duration, traffic_folder):
    # Create the traffic folder if it does not exist
    os.makedirs(traffic_folder, exist_ok=True)

    # List and sort all WAV files in the specified folder
    audio_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.wav')]
    audio_files.sort()

    for i, file_path in enumerate(audio_files):
        print(f"Playing file {i+1}/{len(audio_files)}: {file_path}")

        # Define the output file path in the traffic_W folder
        output_file_path = os.path.join(traffic_folder, f"traffic_capture_{i+1}.pcap")

        # Start the traffic capture in a separate thread
        capture_thread = threading.Thread(target=capture_traffic, args=(duration, output_file_path))
        capture_thread.start()

        # Wait a moment to ensure tcpdump starts before the audio
        time.sleep(1)

        # Play the audio file
        play_audio(file_path)

        # Wait for the capture to finish
        capture_thread.join()
        print(f"Finished playing {file_path} and capturing traffic.")

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Play WAV files from a folder and capture network traffic.')

    # Hardcode folder and duration
    audio_folder = './audio_A'
    capture_duration = 15
    traffic_folder = './traffic_W'
    
    main(audio_folder, capture_duration, traffic_folder)
