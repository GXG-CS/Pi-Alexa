import argparse
import os
import torch
import torchaudio
from scipy.io.wavfile import write

def load_waveglow(device):
    waveglow = torch.hub.load(
        "NVIDIA/DeepLearningExamples:torchhub",
        "nvidia_waveglow",
        model_math="fp32",
        pretrained=False,
    )
    checkpoint = torch.hub.load_state_dict_from_url(
        "https://api.ngc.nvidia.com/v2/models/nvidia/waveglowpyt_fp32/versions/1/files/nvidia_waveglowpyt_fp32_20190306.pth",
        progress=False,
        map_location=device,
    )
    state_dict = {key.replace("module.", ""): value for key, value in checkpoint["state_dict"].items()}

    waveglow.load_state_dict(state_dict)
    waveglow = waveglow.remove_weightnorm(waveglow)
    waveglow = waveglow.to(device)
    waveglow.eval()
    return waveglow

def generate_audio(text_dir, audio_dir, model_choice):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    if model_choice == "WAVEGLOW":
        bundle = torchaudio.pipelines.TACOTRON2_WAVERNN_PHONE_LJSPEECH  # Assuming WaveRNN bundle for preprocessing
        waveglow = load_waveglow(device)  # Load WaveGlow model
    elif model_choice == "WAVERNN":
        bundle = torchaudio.pipelines.TACOTRON2_WAVERNN_PHONE_LJSPEECH
    elif model_choice == "GRIFFINLIM":
        bundle = torchaudio.pipelines.TACOTRON2_GRIFFINLIM_PHONE_LJSPEECH
    else:
        raise ValueError("Invalid model choice.")
    
    processor = bundle.get_text_processor()
    tacotron2 = bundle.get_tacotron2().to(device)
    
    if model_choice != "WAVEGLOW":
        vocoder = bundle.get_vocoder().to(device)

    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)

    for text_file in sorted(os.listdir(text_dir)):
        if text_file.endswith('.txt'):
            file_number = text_file.split('.')[0]
            # Include model_choice in the file name
            audio_file = f"{audio_dir}/{file_number}_{model_choice.lower()}_audio.wav"
            
            with open(f"{text_dir}/{text_file}", 'r') as f:
                text = f.read()

            with torch.inference_mode():
                processed, lengths = processor(text)
                processed = processed.to(device)
                lengths = lengths.to(device)
                spec, spec_lengths, _ = tacotron2.infer(processed, lengths)

            if model_choice == "WAVEGLOW":
                with torch.no_grad():
                    waveforms = waveglow.infer(spec)
            else:
                waveforms, _ = vocoder(spec, spec_lengths)

            audio_numpy = waveforms[0].cpu().numpy()
            rate = 22050  # Common sample rate for TTS models
            write(audio_file, rate, audio_numpy)

    print("Audio files have been saved successfully.")

def main():
    parser = argparse.ArgumentParser(description="TTS Generator")
    parser.add_argument('--text_dir', type=str, required=True)
    parser.add_argument('--audio_dir', type=str, required=True)
    parser.add_argument('--model', type=str, choices=['WAVERNN', 'GRIFFINLIM', 'WAVEGLOW'], required=True)
    args = parser.parse_args()

    generate_audio(args.text_dir, args.audio_dir, args.model)

if __name__ == "__main__":
    main()

# python TTS2.py --text_dir test_text_A --audio_dir test_audio_A --model GRIFFINLIM