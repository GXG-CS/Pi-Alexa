import argparse
import subprocess
import os
import time

def run_remote_audio(remote_username, remote_ip, remote_audio_dir, password):
    try:
        play_command = f"sshpass -p {password} ssh {remote_username}@{remote_ip} 'afplay {remote_audio_dir}'"
        subprocess.run(play_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running remote command: {e}")

def start_traffic_capture(capture_file):
    subprocess.Popen(f"sudo tcpdump -i wlan0 -w {capture_file} &", shell=True)
    print("Started traffic capture.")

def stop_traffic_capture():
    subprocess.run("sudo pkill -SIGINT tcpdump", shell=True)
    print("Stopped traffic capture.")

def main():
    parser = argparse.ArgumentParser(description="Remote Audio Player and Traffic Capturer")
    parser.add_argument('--remote_username', type=str, required=True)
    parser.add_argument('--remote_ip', type=str, required=True)
    parser.add_argument('--remote_audio_dir', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)
    parser.add_argument('--capture_file', type=str, required=True)
    args = parser.parse_args()

    start_traffic_capture(args.capture_file)

    # Run audio playback for a single file
    run_remote_audio(args.remote_username, args.remote_ip, args.remote_audio_dir, args.password)
    time.sleep(12)  # Adjust sleep time as per the length of the audio file

    stop_traffic_capture()

if __name__ == "__main__":
    main()

# python remote_playAudio.py --remote_username xiaoguang_guo@mines.edu --remote_ip 192.168.1.232 --remote_audio_dir /Users/xiaoguang_guo@mines.edu/Documents/Pi-Alexa/data_collection/audio_A/1_audio.wav --password 338166 --capture_file traffic_W/traffic_capture_1.pcap
