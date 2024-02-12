import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# Path to the audio file
audio_file_path = 'audioRecord_C/recorded_5_audio.wav'

try:
    # Use the audio file as the audio source
    with sr.AudioFile(audio_file_path) as source:
        # Record the audio file
        audio_data = recognizer.record(source)
        # Recognize the content of the audio file
        # Specify the language if needed, e.g., "en-US" for American English
        text = recognizer.recognize_google(audio_data, language="en-US")
        print(f"Transcription: {text}")
except sr.RequestError as e:
    # Handle API request errors
    print(f"Could not request results from Google Speech Recognition service; {e}")
except sr.UnknownValueError:
    # Handle errors for unknown words in the audio
    print("Google Speech Recognition could not understand the audio. Consider checking the audio file's quality or specifying the correct language.")
