import torch
import os
from TTS.api import TTS

# Directories setup
text_files_directory = "test/text_A"  # Your text files directory
base_audio_files_directory = "test/audioPlay_A"  # Your base audio files directory

# Selected English models
models = [
    # "tts_models/en/vctk/vits",  # VITS model trained on the VCTK dataset
    # "tts_models/en/sam/tacotron-DDC",  # Tacotron model adapted for the SAM dataset
    # "tts_models/en/blizzard2013/capacitron-t2-c50",  # Tacotron 2 model trained on Blizzard 2013 dataset
    # "tts_models/en/jenny/jenny",  # Specific model trained to mimic "Jenny"
    # "tts_models/en/multi-dataset/tortoise-v2",  # Model trained across multiple datasets
    # "tts_models/en/ljspeech/vits--neon",  # VITS variant trained on LJSpeech
    # "tts_models/en/ljspeech/speedy-speech",  # Speedy Speech model for faster synthesis on LJSpeech
    # "tts_models/en/vctk/fast_pitch",  # Model focusing on pitch control on VCTK
    # "tts_models/en/ljspeech/tacotron2-DCA",  # Tacotron 2 with duration-controlled attention on LJSpeech
    # "tts_models/en/ljspeech/neural_hmm"  # Neural HMM-based model on LJSpeech
]


# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize the TTS for each model and process text files
for model_name in models:
    # Sanitize model name for filesystem
    safe_model_name = model_name.replace("/", "_").replace(":", "_")
    
    # Create model specific audio directory
    audio_files_directory = os.path.join(base_audio_files_directory, safe_model_name)
    if not os.path.exists(audio_files_directory):
        os.makedirs(audio_files_directory)

    # Initialize the TTS with the current model
    tts = TTS(model_name).to(device)

    # Process each text file in the directory
    for text_file in os.listdir(text_files_directory):
        if text_file.endswith('.txt'):  # Ensure processing only text files
            text_file_path = os.path.join(text_files_directory, text_file)
            # Read the text from the text file
            with open(text_file_path, 'r') as f:
                text = f.read()

            # Generate the audio file name
            audio_file_name = f"{text_file.replace('.txt', '')}_{safe_model_name}.wav"
            audio_file_path = os.path.join(audio_files_directory, audio_file_name)

            # Text to speech to a file
            print(f"Synthesizing {text_file_path} using model {model_name}")
            tts.tts_to_file(text=text, file_path=audio_file_path)
            print(f"Output saved to {audio_file_path}")
