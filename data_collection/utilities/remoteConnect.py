import paramiko
import argparse

def run_command_on_pi(ip, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect using a password
    ssh.connect(ip, username=username, password=password)

    stdin, stdout, stderr = ssh.exec_command(command)

    # Wait for the command to complete and capture the output
    stdout.channel.recv_exit_status()
    output = stdout.read().decode()
    error = stderr.read().decode()

    print("Command Output:\n", output)
    if error:
        print("Command Error:\n", error)
    else:
        print("Command executed successfully.")

    ssh.close()

def main():
    parser = argparse.ArgumentParser(description='Run a command on a Raspberry Pi via SSH.')
    parser.add_argument('ip', type=str, help='IP address of the Raspberry Pi')
    parser.add_argument('username', type=str, help='Username for SSH login')
    parser.add_argument('password', type=str, help='Password for SSH login')
    parser.add_argument('command', type=str, help='Command to run on the Raspberry Pi')

    args = parser.parse_args()

    run_command_on_pi(args.ip, args.username, args.password, args.command)

if __name__ == "__main__":
    main()


# python remoteConnect.py 192.168.1.167 root raspberry "nohup tcpdump -i any -w /opt/tcpdump/audio4.pcap &"
# python remoteConnect.py 192.168.1.167 root raspberry "pkill -SIGINT tcpdump"