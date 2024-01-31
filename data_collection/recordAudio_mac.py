import sounddevice as sd
import numpy as np
import wavio

# Function to list available devices
# def list_devices():
#     print("Available audio devices:")
#     print(sd.query_devices())

def record_audio(filename, duration=5, fs=44100, channels=1):
    print("Recording...")

    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()  # Wait until recording is finished

    wavio.write(filename, audio_data, fs, sampwidth=2)

    print(f"Recording finished, file saved as {filename}")

# List available devices
# list_devices()

# Recording settings
output_file = 'output.wav'
record_seconds = 5
record_audio(output_file, record_seconds)
