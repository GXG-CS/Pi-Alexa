import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os
from datetime import datetime

def preprocess_timestamp(timestamp_str):
    # Extract the datetime portion up to the microseconds
    # Assuming the format is consistent as "Feb 14, 2024 10:26:56.015662000 Mountain Standard Time"
    # Remove the timezone information and the extra precision in microseconds
    datetime_str = ' '.join(timestamp_str.split()[:3]) + ' ' + timestamp_str.split()[3].split('.')[0]
    # Keep only up to 6 digits for microseconds
    datetime_str += '.' + timestamp_str.split()[3].split('.')[1][:6]
    return datetime_str

def parse_timestamp(timestamp_str):
    datetime_str = preprocess_timestamp(timestamp_str)
    try:
        return datetime.strptime(datetime_str, '%b %d, %Y %H:%M:%S.%f')
    except ValueError as e:
        print(f"Error parsing timestamp '{timestamp_str}': {e}")
        return None

def plot_traffic(file_path, plot_dir, file_name, traffic_type):
    df = pd.read_csv(file_path)
    df['frame.time'] = df['frame.time'].apply(parse_timestamp)
    df.dropna(subset=['frame.time'], inplace=True)
    df.set_index(pd.DatetimeIndex(df['frame.time']), inplace=True)
    counts = df.resample('s').size().head(10)

    # Check if there is data to plot
    if not counts.empty:
        # Plot the data
        plt.plot(range(len(counts)), counts.values, marker='o', label=f'{traffic_type} {file_name}')

def main():
    parser = argparse.ArgumentParser(description='Plot and save network traffic data.')
    parser.add_argument('--dir_incoming', type=str, required=True, help='Directory with incoming traffic CSV files')
    parser.add_argument('--dir_outgoing', type=str, required=True, help='Directory with outgoing traffic CSV files')
    parser.add_argument('--plot_dir', type=str, required=True, help='Directory to save the plots')
    args = parser.parse_args()

    if not os.path.exists(args.plot_dir):
        os.makedirs(args.plot_dir)

    # Plot incoming traffic
    for file_name in os.listdir(args.dir_incoming):
        if file_name.endswith('.csv'):
            file_path = os.path.join(args.dir_incoming, file_name)
            plt.figure(figsize=(14, 7))
            plot_traffic(file_path, args.plot_dir, file_name.replace('.csv', ''), 'Incoming')

            # Plot outgoing traffic
            corresponding_outgoing_file = file_name.replace('incoming', 'outgoing')
            outgoing_file_path = os.path.join(args.dir_outgoing, corresponding_outgoing_file)
            if os.path.exists(outgoing_file_path):
                plot_traffic(outgoing_file_path, args.plot_dir, corresponding_outgoing_file.replace('.csv', ''), 'Outgoing')
            
            plt.title(f'Network Traffic Analysis for {file_name}')
            plt.xlabel('Time (second)')
            plt.ylabel('Number of Packets')
            plt.legend()
            plt.grid(True)

            plot_name = f'{file_name.replace(".csv", "")}_plot.png'
            plt.savefig(os.path.join(args.plot_dir, plot_name))
            plt.close()

if __name__ == "__main__":
    main()


# import pandas as pd
# import matplotlib.pyplot as plt
# import argparse
# import os
# from datetime import datetime

# def preprocess_timestamp(timestamp_str):
#     # Extract the datetime portion up to the microseconds
#     # Assuming the format is consistent as "Feb 14, 2024 10:26:56.015662000 Mountain Standard Time"
#     # Remove the timezone information and the extra precision in microseconds
#     datetime_str = ' '.join(timestamp_str.split()[:3]) + ' ' + timestamp_str.split()[3].split('.')[0]
#     # Keep only up to 6 digits for microseconds
#     datetime_str += '.' + timestamp_str.split()[3].split('.')[1][:6]
#     return datetime_str

# def parse_timestamp(timestamp_str):
#     datetime_str = preprocess_timestamp(timestamp_str)
#     # Parse the preprocessed timestamp string into a datetime object
#     try:
#         return datetime.strptime(datetime_str, '%b %d, %Y %H:%M:%S.%f')
#     except ValueError as e:
#         print(f"Error parsing timestamp '{timestamp_str}': {e}")
#         return None


# def plot_traffic(file_path, plot_dir, file_name):
#     df = pd.read_csv(file_path)
#     df['frame.time'] = df['frame.time'].apply(parse_timestamp)
#     df.dropna(subset=['frame.time'], inplace=True)
#     df.set_index(pd.DatetimeIndex(df['frame.time']), inplace=True)
#     counts = df.resample('s').size()

#     # Check if there is data to plot
#     if not counts.empty:
#         plt.figure(figsize=(14, 7))
#         seconds_to_plot = min(len(counts), 10)  # Determine the number of seconds to plot (up to 10)
#         plt.plot(range(seconds_to_plot), counts.head(seconds_to_plot).values, marker='o', label=f'{file_name} Traffic')
#         plt.title(f'Network Traffic Analysis for {file_name}')
#         plt.xlabel('Time (second)')
#         plt.ylabel('Number of Packets')
#         plt.legend()
#         plt.grid(True)

#         plot_name = f'{file_name}_plot.png'
#         plot_path = os.path.join(plot_dir, plot_name)
#         plt.savefig(plot_path)
#         plt.close()
#         print(f"Plot saved to {plot_path}")


# def main():
#     parser = argparse.ArgumentParser(description='Plot and save network traffic data.')
#     parser.add_argument('--dir_incoming', type=str, required=True, help='Directory with incoming traffic CSV files')
#     parser.add_argument('--dir_outgoing', type=str, required=True, help='Directory with outgoing traffic CSV files')
#     parser.add_argument('--plot_dir', type=str, required=True, help='Directory to save the plots')
#     args = parser.parse_args()

#     if not os.path.exists(args.plot_dir):
#         os.makedirs(args.plot_dir)

#     for traffic_dir in [args.dir_incoming, args.dir_outgoing]:
#         for file_name in os.listdir(traffic_dir):
#             if file_name.endswith('.csv'):
#                 file_path = os.path.join(traffic_dir, file_name)
#                 plot_traffic(file_path, args.plot_dir, file_name.replace('.csv', ''))

# if __name__ == "__main__":
#     main()

# python plot_traffic.py --dir_incoming "traffic_W_incoming_csv" --dir_outgoing "traffic_W_outgoing_csv" --plot_dir "traffic_W_plot"
