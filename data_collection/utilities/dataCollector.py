import os
import subprocess
import sounddevice as sd
import wavio
import argparse
import paramiko
import time
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
    subprocess.call(["afplay", file])

def record_audio(filename, duration=10, fs=44100, channels=1):
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()  # Wait until recording is finished
    wavio.write(filename, audio_data, fs, sampwidth=2)

def main(ip, username, password, audio_dir, record_dir, record_duration, key_filepath=None):
    if not os.path.exists(record_dir):
        os.makedirs(record_dir)

    with SSHConnection(ip, username, password, key_filepath) as ssh:
        for audio_file in os.listdir(audio_dir):
            if audio_file.endswith('.wav'):
                full_audio_path = os.path.join(audio_dir, audio_file)
                pcap_filename = f"/opt/tcpdump/{os.path.splitext(audio_file)[0]}.pcap"

                # Start capture
                print(f"{get_timestamp()}: Starting capture")
                tcpdump_command = f"nohup tcpdump -i any -w {pcap_filename} &"
                ssh.execute_command(tcpdump_command)

                # Play audio and record the start time
                print(f"{get_timestamp()}: Playing {audio_file}")
                start_time = datetime.now()
                play_audio(full_audio_path)

                # Record audio
                record_file = os.path.join(record_dir, f"recorded_{os.path.splitext(audio_file)[0]}.wav")
                print(f"{get_timestamp()}: Recording {audio_file} for {record_duration} seconds")
                record_audio(record_file, duration=record_duration)

                # Calculate elapsed time and wait for the remaining time of the 20-second window
                elapsed_time = (datetime.now() - start_time).total_seconds()
                remaining_time = max(20 - elapsed_time, 0)
                if remaining_time > 0:
                    time.sleep(remaining_time)

                # Stop capture
                print(f"{get_timestamp()}: Stopping capture")
                ssh.execute_command("pkill -SIGINT tcpdump")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Play audio files and record with network traffic capture on Raspberry Pi.')
    parser.add_argument('--ip', type=str, required=True, help='IP address of the Raspberry Pi')
    parser.add_argument('--username', type=str, required=True, help='Username for SSH login')
    parser.add_argument('--password', type=str, help='Password for SSH login')
    parser.add_argument('--key_filepath', type=str, help='SSH key file path')
    parser.add_argument('--audio_dir', type=str, default='audioPlay_A_old', help='Directory containing audio files to play')
    parser.add_argument('--record_dir', type=str, default='audioRecord', help='Directory to save recorded audio')
    parser.add_argument('--duration', type=int, default=10, help='Duration of the recording in seconds')
    args = parser.parse_args()

    main(args.ip, args.username, args.password, args.audio_dir, args.record_dir, args.duration, args.key_filepath)
