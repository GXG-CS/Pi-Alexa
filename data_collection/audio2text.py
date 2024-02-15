import speech_recognition as sr
import argparse
import os

def recognize_speech_from_audio(audio_dir, text_dir):
    # Ensure the audio directory exists
    if not os.path.exists(audio_dir):
        print(f"The directory {audio_dir} does not exist.")
        return
    
    # Ensure the text directory exists
    if not os.path.exists(text_dir):
        os.makedirs(text_dir)

    # Create a speech recognizer
    recognizer = sr.Recognizer()
    
    # Process each .wav file in the directory
    for audio_file in os.listdir(audio_dir):
        if audio_file.endswith('.wav'):
            try:
                # Load the audio file
                path_to_audio = os.path.join(audio_dir, audio_file)
                with sr.AudioFile(path_to_audio) as source:
                    audio_data = recognizer.record(source)

                # Recognize speech using Sphinx
                text = recognizer.recognize_sphinx(audio_data)
                
                # Define the output text filename
                base_name = os.path.splitext(audio_file)[0]
                text_filename = os.path.join(text_dir, f"{base_name}_text.txt")

                # Save the recognized text to a file
                with open(text_filename, 'w') as text_file:
                    text_file.write(text)

                print(f"Processed {audio_file}")
                
            except sr.UnknownValueError:
                print(f"Could not understand audio from {audio_file}")
            except sr.RequestError as e:
                print(f"Error with Sphinx recognition from {audio_file}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Convert audio files to text using speech recognition.')
    parser.add_argument('--audio_dir', type=str, required=True, help='Directory containing audio files to process')
    parser.add_argument('--text_dir', type=str, required=True, help='Directory to save the resulting text files')
    args = parser.parse_args()

    recognize_speech_from_audio(args.audio_dir, args.text_dir)

if __name__ == "__main__":
    main()

# python audio2text.py --audio_dir "test/audioRecord_C" --text_dir "test/text_C"
