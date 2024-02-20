import os
import pandas as pd

# Function to check if the text file is empty
def is_text_file_empty(file_path):
    return os.path.getsize(file_path) == 0

# Function to check if the CSV file is empty
def is_csv_file_empty(file_path):
    try:
        df = pd.read_csv(file_path)
        return df.empty
    except pd.errors.EmptyDataError:
        return True

# Preprocess data
def preprocess_data(file_count, text_folder, traffic_data_folder):
    valid_data_indices = []

    for i in range(1, file_count + 1):
        text_file = os.path.join(text_folder, f"{i}.txt")
        traffic_data_file = os.path.join(traffic_data_folder, f"{i}_tts_models_en_ljspeech_tacotron2-DCA_outgoing_text_time_series.csv")
        
        # Check if either the text file or CSV file is empty
        if not is_text_file_empty(text_file) and not is_csv_file_empty(traffic_data_file):
            valid_data_indices.append(i)
    
    return valid_data_indices

# Example usage
if __name__ == "__main__":
    file_count = 1000  # Total number of data pieces
    text_folder = '../data_collection/ground_truth/text_A' 
    traffic_data_folder = '../data_collection/ground_truth/outgoing/traffic_W_outgoing_timeSeries' 
    
    # Get the indices of valid data pairs
    valid_indices = preprocess_data(file_count, text_folder, traffic_data_folder)
    
    # Output the number of valid data pairs
    print(f"Number of valid data pairs: {len(valid_indices)}")

