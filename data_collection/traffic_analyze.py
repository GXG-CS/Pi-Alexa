import pandas as pd
import os
import argparse

def clean_timestamps(input_file, output_file, direction):
    # Load the CSV file
    df = pd.read_csv(input_file)

    # Remove the timezone from the 'frame.time' column
    df['frame.time'] = df['frame.time'].str.replace(' Mountain Standard Time', '', regex=False)

    # Convert the 'frame.time' to datetime objects, coercing errors
    df['frame.time'] = pd.to_datetime(df['frame.time'], errors='coerce')

    # Drop rows where the time could not be parsed
    df = df.dropna(subset=['frame.time'])

    # Subtract the minimum time from all times to reset starting time to 0
    df['t'] = (df['frame.time'] - df['frame.time'].min()).dt.total_seconds()

    # Select the 'frame.len' as 'l' and drop all other columns
    df_final = df[['t', 'frame.len']].rename(columns={'frame.len': 'l'})

    # Set the direction for all entries
    df_final['d'] = direction

    # Save the final DataFrame to the new CSV file
    df_final.to_csv(output_file, index=False)
    print(f"Converted {input_file} to {output_file}")

def main(input_dir, output_dir, direction):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each CSV file in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.csv'):
            input_file_path = os.path.join(input_dir, file_name)
            output_file_name = os.path.splitext(file_name)[0] + '_time_series.csv'
            output_file_path = os.path.join(output_dir, output_file_name)
            clean_timestamps(input_file_path, output_file_path, direction)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert timestamps in CSV files to time series data with direction.')
    parser.add_argument('--input_dir', type=str, required=True, help='Directory containing input .csv files')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save the converted .csv files')
    parser.add_argument('--direction', type=int, default=1, help='Direction of traffic (1 for incoming, 0 for outgoing)')
    args = parser.parse_args()

    main(args.input_dir, args.output_dir, args.direction)

# python traffic_analyze.py --input_dir traffic_W_incoming_csv --output_dir traffic_W_incoming_timeSeries --direction 1
# python traffic_analyze.py --input_dir traffic_W_outgoing_csv --output_dir traffic_W_outgoing_timeSeries --direction 0