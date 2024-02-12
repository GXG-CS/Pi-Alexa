import pyaudio
import wave

def record_audio(record_seconds, output_filename):
    # Audio recording parameters
    FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
    CHANNELS = 1              # Mono audio
    RATE = 44100              # Sample rate (44.1kHz)
    CHUNK = 1024              # Frames per buffer

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open stream for recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    # Start recording
    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate the PyAudio object
    audio.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"File saved: {output_filename}")

# Example usage
# if __name__ == "__main__":
#     record_seconds = 5  # Duration of recording in seconds
#     output_filename = "recorded_file.wav"  # Output filename
#     record_audio(record_seconds, output_filename)
