import subprocess
import argparse
import os

def pcap_to_csv(pcap_file, csv_file):
    # Define the tshark command to run
    command = [
        "tshark",
        "-r", pcap_file,
        "-T", "fields",
        "-e", "frame.number",
        "-e", "frame.time",  # includes the timestamp in the requested format
        "-e", "ip.src",
        "-e", "ip.dst",
        "-e", "_ws.col.Protocol",
        "-e", "frame.len",
        "-E", "header=y",
        "-E", "separator=,",
        "-E", "quote=d",
        "-E", "occurrence=f"
    ]
    
    # Run the command and save output to csv_file
    with open(csv_file, 'w') as output_file:
        subprocess.run(command, stdout=output_file, text=True)
    
    print(f"Converted {pcap_file} to {csv_file}")

def main():
    parser = argparse.ArgumentParser(description='Convert .pcap files to .csv format for analysis with timestamp.')
    parser.add_argument('--pcap_dir', type=str, required=True, help='Directory containing .pcap files to process')
    parser.add_argument('--csv_dir', type=str, required=True, help='Directory to save the resulting .csv files')
    args = parser.parse_args()

    # Ensure the CSV directory exists
    if not os.path.exists(args.csv_dir):
        os.makedirs(args.csv_dir)
    
    # Convert each .pcap file in the directory
    for file_name in os.listdir(args.pcap_dir):
        if file_name.endswith('.pcap'):
            pcap_path = os.path.join(args.pcap_dir, file_name)
            csv_file_name = os.path.splitext(file_name)[0] + '_text.csv'
            csv_path = os.path.join(args.csv_dir, csv_file_name)
            pcap_to_csv(pcap_path, csv_path)

if __name__ == "__main__":
    main()

# python pcap2csv.py --pcap_dir "traffic_W_outgoing" --csv_dir "traffic_W_outgoing_csv"

