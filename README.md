# Data Collection Component

## Overview
The data collection component is responsible for gathering the necessary data to train the model that infers interactions with Alexa. This involves establishing a secure connection between a MAC and a Raspberry Pi to capture traffic data, converting audio responses to text, and preparing the data for analysis.

## Scripts Description

- `audio2text.py`: Converts recorded Alexa response audio files into text files. This is crucial for creating datasets that pair spoken commands with their text representation.

- `coqui_tts.py`: Uses the Coqui TTS library to synthesize speech from text. This allows for the generation of voice commands that can be used to interact with Alexa.

- `dataCollector2.py`: Establishes an SSH connection between a MAC and a Raspberry Pi, which is configured as an OpenWRT VPN-enabled router. It plays voice command audio files to interact with Alexa on the MAC, records Alexa's responses, and controls the capture of traffic data on the Raspberry Pi automatically.

- `parallel_coqui_tts.py`: Runs the text-to-speech (TTS) synthesis in parallel using `torch.multiprocessing` to improve efficiency when generating large datasets.

- `pcap2csv.py`: Converts captured traffic data in PCAP format to CSV for further analysis. This transformation is essential for data preprocessing and model input.

- `plot_traffic.py`: Provides visualization of the traffic data, offering insights into the patterns of data exchange between Alexa and the network.

- `traffic_analyze.py`: Transforms traffic data in CSV format into time series data, preparing the dataset for time series analysis and model training.

- `traffic_filter.py`: Filters raw traffic data to isolate the exchanges between Alexa and the VPN, ensuring the dataset focuses on relevant interactions.
