import torch
import torchaudio
import IPython.display as ipd
import matplotlib.pyplot as plt
from scipy.io.wavfile import write


# Set the device to CUDA if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load pre-trained Tacotron2 and vocoder models
bundle = torchaudio.pipelines.TACOTRON2_WAVERNN_PHONE_LJSPEECH
processor = bundle.get_text_processor()
tacotron2 = bundle.get_tacotron2().to(device)
vocoder = bundle.get_vocoder().to(device)

# text to synthesize
text = "Hello world! Text to speech! fsfsdfsf"

# Process text and generate spectrogram
with torch.inference_mode():
    processed, lengths = processor(text)
    processed = processed.to(device)
    lengths = lengths.to(device)
    spec, spec_lengths, _ = tacotron2.infer(processed, lengths)

# Convert spectrogram to waveform
waveforms, _ = vocoder(spec, spec_lengths)

# Convert waveform to numpy array and get sample rate
audio_numpy = waveforms[0].cpu().numpy()
rate = vocoder.sample_rate

# Save the audio to a WAV file
audio_path = "output_audio.wav"
write(audio_path, rate, audio_numpy)