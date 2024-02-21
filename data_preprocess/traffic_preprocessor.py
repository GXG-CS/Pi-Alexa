import pandas as pd
from pathlib import Path
import pickle

def load_traffic_time_series_data(traffic_data_directory):
    # Sort files by the numerical value in their filename
    file_paths = sorted(Path(traffic_data_directory).glob('*.csv'), key=lambda path: int(path.stem.split('_')[0]))
    traffic_data_as_tuples = []

    for file_path in file_paths:
        print(f"Loading file: {file_path.name}")  # Print the current file name
        traffic_df = pd.read_csv(file_path)
        # Assuming each file contains columns 't' for time, 'l' for length, and 'd' for direction
        # Convert DataFrame to a list of tuples (t, l, d)
        traffic_tuples = list(traffic_df.itertuples(index=False, name=None))
        traffic_data_as_tuples.append(traffic_tuples)

    return traffic_data_as_tuples

# Example usage
if __name__ == "__main__":
    traffic_data_directory = '../data_collection/ground_truth/outgoing/traffic_W_outgoing_timeSeries'
    traffic_data_as_tuples = load_traffic_time_series_data(traffic_data_directory)
    
    # Optionally, print some of the loaded data to verify
    # Print the first tuple from the first file as an example
    # Save the list of tuples using pickle
    with open('processed_data/traffic_data_tuples.pkl', 'wb') as f:
        pickle.dump(traffic_data_as_tuples, f)

    print("Traffic data has been saved to 'processed_data/traffic_data_tuples.pkl'.")
