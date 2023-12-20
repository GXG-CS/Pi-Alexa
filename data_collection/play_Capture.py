import argparse
import subprocess
import threading
import time
from scapy.all import sniff, IP, wrpcap
from datetime import datetime

SLEEP_TIME = 10  # Sleep for 2 seconds before playing the audio
DURATION = 10   # Capture for 10 seconds during and after audio playback

def play_audio(file_path):
    try:
        print("Starting audio playback...")
        subprocess.run(['aplay', file_path], check=True)
        print("Audio playback has ended.")
    except subprocess.CalledProcessError as e:
        print(f"Error playing audio: {e}")

def packet_handler(packet):
    if IP in packet:
        timestamp = datetime.fromtimestamp(packet.time).strftime('%Y-%m-%d %H:%M:%S.%f')
        print(f"Packet: {timestamp}, Source: {packet[IP].src}, Destination: {packet[IP].dst}, Length: {len(packet)}")

def capture_traffic(interface, output_file, duration):
    print("Starting traffic capture...")
    packets = sniff(iface=interface, prn=packet_handler, timeout=duration)
    print("Traffic capture has ended.")
    wrpcap(output_file, packets)
    print("Packets saved to {} successfully.".format(output_file))

def sleep_with_announcements():
    print("Entering sleep period...")
    for i in range(SLEEP_TIME):
        time.sleep(1)
        print(f"Slept for {i + 1} seconds...")
    print("Exiting sleep period.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Play a WAV file and capture network traffic.')
    parser.add_argument('file_path', type=str, help='Path to the WAV file to play.')
    parser.add_argument('output_file', type=str, help='Path to save the traffic capture file.')

    args = parser.parse_args()

    # Start traffic capture in a separate thread immediately
    capture_thread = threading.Thread(target=capture_traffic, args=('wlan0', args.output_file, DURATION + SLEEP_TIME))
    capture_thread.start()

    # Sleep with announcements
    sleep_with_announcements()

    # Play the audio file
    play_audio(args.file_path)

    # Wait for the capture thread to finish
    capture_thread.join()

    print("Script has completed all operations.")




# sudo python play_Capture.py audio_A/7_audio.wav traffic_W/test7.pcap 