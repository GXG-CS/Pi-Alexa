import os
import time
import subprocess
import pygame

# Initialize the mixer module
pygame.mixer.init()

# Set your directories
audio_dir = 'path/to/your/audio_files'

# List of audio files
audio_files = sorted([f for f in os.listdir(audio_dir) if f.endswith('.wav')])

# Function to play audio
def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)

# Play audio files one by one
for audio_file in audio_files:
    full_path = os.path.join(audio_dir, audio_file)
    print(f"Playing {audio_file}")
    play_audio(full_path)
    # Start traffic capture here
    # subprocess.Popen(['sudo', 'tcpdump', '-i', 'eth0', '-w', f'path/to/your/traffic_data/{audio_file}.pcap'])
    # Wait for the duration of the audio file
    # time.sleep(audio_duration)
    # Stop traffic capture here
    # subprocess.Popen(['sudo', 'pkill', 'tcpdump'])
    print(f"Finished playing {audio_file}")
