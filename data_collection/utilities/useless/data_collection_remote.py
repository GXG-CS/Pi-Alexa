import subprocess
import os

def run_play_audio_script(script_path, remote_username, remote_ip, audio_file_path, password, capture_file):
    command = f"python {script_path} --remote_username {remote_username} --remote_ip {remote_ip} --remote_audio_dir {audio_file_path} --password {password} --capture_file {capture_file}"
    subprocess.run(command, shell=True)

def main():
    script_path = 'remote_playAudio.py'
    remote_username = 'xiaoguang_guo@mines.edu'
    remote_ip = '192.168.1.232'
    remote_audio_dir = '/Users/xiaoguang_guo@mines.edu/Documents/Pi-Alexa/data_collection/audio_A'
    password = '338166'
    capture_dir = ' traffic_W'

    total_files = 101
    for i in range(10, total_files + 1):
        audio_file_name = f"{remote_audio_dir}/{i}_audio.wav"
        capture_file = f"{capture_dir}/{i}_traffic.pcap"
        run_play_audio_script(script_path, remote_username, remote_ip, audio_file_name, password, capture_file)



if __name__ == "__main__":
    main()
