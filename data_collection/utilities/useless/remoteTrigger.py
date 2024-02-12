import paramiko
import time

def start_alexa_and_tap(hostname, port, username, password):
    try:
        # Set up SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password)

        # Use invoke_shell to simulate a terminal session
        shell = ssh.invoke_shell()
        
        # Start the Alexa app
        shell.send('cd $HOME/sdk-folder/sdk-build/\n')
        shell.send('./SampleApplications/ConsoleSampleApplication/src/SampleApp ./Integration/AlexaClientSDKConfig.json\n')
        
        # Wait for the app to initialize (adjust time as needed)
        time.sleep(5)  # Wait time might need to be adjusted based on your app's startup time
        
        # Simulate pressing 't'
        shell.send('t\n')

        print("Alexa app started and 't' simulated")
        
        # Wait a bit to see if there's any immediate output/response
        time.sleep(5)
        
        # Capture the output (this part may need customization based on your needs)
        output = shell.recv(10000)
        print(output.decode())

        # Close the shell and connection
        shell.close()
        ssh.close()

    except Exception as e:
        print(f"An error occurred: {e}")

# Configuration - replace with your details
hostname = '192.168.1.155'  # Raspberry Pi's hostname or IP address
port = 22  # Default SSH port
username = 'pi'  # Default Raspberry Pi username
password = 'raspberry'  # SSH password for Raspberry Pi

# Start the Alexa app and simulate 'tap'
start_alexa_and_tap(hostname, port, username, password)
