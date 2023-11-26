from detect_traffic import start_traffic_detection
# from recording import record_audio
import threading
import time

# Parameters for traffic detection and audio recording
INTERFACE = 'wlan0'
MONITOR_IP = '10.3.141.158'  # Replace with the IP you want to monit or
# RECORD_SECONDS = 10
# OUTPUT_FILENAME = 'traffic_audio.wav'

def monitor_traffic_and_record():
    # Start a separate thread for traffic detection
    traffic_thread = threading.Thread(target=start_traffic_detection, args=(INTERFACE, MONITOR_IP))
    traffic_thread.start()

    # Wait for a certain condition or a specific event
    # For example, wait for 30 seconds before starting recording
    # time.sleep(30)

    # Start audio recording
    print("Starting audio recording...")
    # record_audio(RECORD_SECONDS, OUTPUT_FILENAME)
    print("Audio recording finished.")

    # Here you can add logic to stop the traffic detection if necessary
    # For example, if you have a mechanism to stop it after a certain event

if __name__ == "__main__":
    monitor_traffic_and_record()
