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

# Data Preprocessing Component

## Overview
The preprocessing component of the pipeline is designed to clean and transform the collected data into a format suitable for feeding into machine learning models. It includes scripts for handling both textual and traffic data, ensuring that empty or irrelevant information is removed and that the data is appropriately structured for analysis.

## Scripts Description

- `preprocessor_removeEmpty.py`: Scans the dataset directories and removes any text (.txt) or CSV files that are empty. This step is crucial to ensure the quality of the datasets and the efficiency of subsequent preprocessing steps.

- `text_preprocessor.py`: Processes the text data by vectorizing the text and saving it as tuples in a .pkl (pickle) file for later use by the machine learning models. The vectorization of text is a critical step for natural language processing tasks.

- `traffic_preprocessor.py`: Converts traffic time series data into a structured format with tuples of (t, l, d), where 't' stands for timestamp, 'l' for length of the traffic interaction, and 'd' for direction, with 1 representing incoming traffic and 0 representing outgoing traffic. This script ensures that the traffic data is in a consistent and analyzable form.
