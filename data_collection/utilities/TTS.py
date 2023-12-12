import argparse
import os
import torch
import torchaudio
from scipy.io.wavfile import write

def generate_audio(text_dir, audio_dir):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    bundle = torchaudio.pipelines.TACOTRON2_WAVERNN_PHONE_LJSPEECH
    processor = bundle.get_text_processor()
    tacotron2 = bundle.get_tacotron2().to(device)
    vocoder = bundle.get_vocoder().to(device)

    # Create audio directory if it doesn't exist
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)

    # Process each text file in the directory
    for text_file in sorted(os.listdir(text_dir)):
        if text_file.endswith('.txt'):
            file_number = text_file.split('.')[0]
            audio_file = f"{audio_dir}/{file_number}_audio.wav"
            
            # Read the text from file
            with open(f"{text_dir}/{text_file}", 'r') as f:
                text = f.read()

            # Generate spectrogram
            with torch.inference_mode():
                processed, lengths = processor(text)
                processed = processed.to(device)
                lengths = lengths.to(device)
                spec, spec_lengths, _ = tacotron2.infer(processed, lengths)

            # Convert spectrogram to waveform
            waveforms, _ = vocoder(spec, spec_lengths)

            # Save the audio
            audio_numpy = waveforms[0].cpu().numpy()
            rate = vocoder.sample_rate
            write(audio_file, rate, audio_numpy)

    print("Audio files have been saved successfully.")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="TTS Generator")
    parser.add_argument('--text_dir', type=str, help='Directory of text files', required=True)
    parser.add_argument('--audio_dir', type=str, help='Directory to save audio files', required=True)
    args = parser.parse_args()

    generate_audio(args.text_dir, args.audio_dir)

if __name__ == "__main__":
    main()
