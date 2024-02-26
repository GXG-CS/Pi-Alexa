import os
import subprocess
import sounddevice as sd
import wavio
import argparse
import paramiko
import time
import threading
from datetime import datetime

class SSHConnection:
    def __init__(self, ip, username, password=None, key_filepath=None):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        if key_filepath:
            self.ssh.connect(ip, username=username, key_filename=key_filepath)
        elif password:
            self.ssh.connect(ip, username=username, password=password)
        else:
            raise ValueError("Must provide either key_filepath or password")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ssh.close()

    def execute_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.read().decode(), stderr.read().decode()

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def play_audio(file):
    print(f"{get_timestamp()}: Starting to play audio file: {file}")
    subprocess.call(["afplay", file])
    print(f"{get_timestamp()}: Finished playing audio file: {file}")

def record_audio(filename, duration=5, fs=44100, channels=1):
    print(f"{get_timestamp()}: Starting to record audio. File will be saved as: {filename}")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()  # Wait until recording is finished
    wavio.write(filename, audio_data, fs, sampwidth=2)
    print(f"{get_timestamp()}: Finished recording audio. File saved as: {filename}")

def play_and_record(ssh, audio_file, audio_dir, record_dir_base, record_duration, repetitions):
    audio_file_base_name = os.path.splitext(audio_file)[0]
    # Create a unique directory for each audio file's recordings
    record_dir = os.path.join(record_dir_base, audio_file_base_name)
    if not os.path.exists(record_dir):
        os.makedirs(record_dir)

    for i in range(repetitions):
        full_audio_path = os.path.join(audio_dir, audio_file)
        # Recordings named sequentially within each audio file's folder
        record_file_name = f"{i+1}.wav"
        record_file = os.path.join(record_dir, record_file_name)
        pcap_dir = f"/opt/tcpdump/{audio_file_base_name}/"
        ssh.execute_command(f"mkdir -p {pcap_dir}")  # Ensure directory for pcap files exists
        pcap_filename = f"{pcap_dir}{i+1}.pcap"

        print(f"{get_timestamp()}: Starting capture of network traffic. Captured data will be saved in: {pcap_filename}")
        tcpdump_command = f"nohup tcpdump -i any -w {pcap_filename} > /dev/null 2>&1 &"
        ssh.execute_command(tcpdump_command)

        play_audio(full_audio_path)
        record_audio(record_file, duration=record_duration)

        time.sleep(5)  # Ensure capture includes the whole interaction

        print(f"{get_timestamp()}: Stopping network traffic capture.")
        ssh.execute_command("ps | grep '[t]cpdump' | awk '{print $1}' | xargs -r kill -SIGINT")

        print(f"{get_timestamp()}: Audio play and record cycle {i+1}/{repetitions} completed for: {audio_file}")

def main(ip, username, password, audio_dir, record_dir, record_duration, repetitions, key_filepath=None):
    if not os.path.exists(record_dir):
        os.makedirs(record_dir)

    with SSHConnection(ip, username, password, key_filepath) as ssh:
        audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.wav')]
        for audio_file in audio_files:
            play_and_record(ssh, audio_file, audio_dir, record_dir, record_duration, repetitions)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Play audio files and record responses with network traffic capture.')
    parser.add_argument('--ip', type=str, required=True, help='IP address of the Raspberry Pi')
    parser.add_argument('--username', type=str, required=True, help='Username for SSH login')
    parser.add_argument('--password', type=str, help='Password for SSH login')
    parser.add_argument('--key_filepath', type=str, help='SSH key file path')
    parser.add_argument('--audio_dir', type=str, required=True, help='Directory containing audio files to play')
    parser.add_argument('--record_dir', type=str, required=True, help='Directory to save recorded audio')
    parser.add_argument('--duration', type=int, default=5, help='Duration of the response recording in seconds')
    parser.add_argument('--repetitions', type=int, default=1000, help='Number of times to repeat playing and recording for each audio file')
    args = parser.parse_args()

    main(args.ip, args.username, args.password, args.audio_dir, args.record_dir, args.duration, args.repetitions, args.key_filepath)

# python dataCollector3.py --ip 192.168.1.1 --username root --password raspberry --audio_dir ground_truth/audioPlay_A --record_dir ground_truth/audioRecord_C