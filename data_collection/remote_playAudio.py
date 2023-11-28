import subprocess

def run_remote_audio(remote_username, remote_ip, remote_audio_path):
    try:
        # Command to activate conda environment and play audio
        command = f"ssh {remote_username}@{remote_ip} 'source activate python3.9; afplay {remote_audio_path}'"
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running remote command: {e}")

def main():
    remote_username = "xiaoguang_guo@mines.edu"
    remote_ip = "192.168.1.232"
    remote_audio_path = "/Users/xiaoguang_guo@mines.edu/Documents/Pi-Alexa/data_collection/audio_A/1_audio.wav"

    run_remote_audio(remote_username, remote_ip, remote_audio_path)

if __name__ == "__main__":
    main()
