import subprocess
import os
import argparse

def ensure_dir_exists(directory):
    """Ensure the specified directory exists, create if not."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def filter_and_save_traffic(pcap_file, alexa_ip, vpn_ip, outgoing_dir, incoming_dir):
    """Filter and save the outgoing and incoming traffic to specified directories."""
    ensure_dir_exists(outgoing_dir)
    ensure_dir_exists(incoming_dir)
    
    base_name = os.path.splitext(os.path.basename(pcap_file))[0]
    outgoing_pcap = os.path.join(outgoing_dir, f"{base_name}_outgoing.pcap")
    incoming_pcap = os.path.join(incoming_dir, f"{base_name}_incoming.pcap")

    # Command for filtering outgoing packets (Alexa to VPN)
    outgoing_command = f"tshark -r \"{pcap_file}\" -Y \"ip.src == {alexa_ip} and ip.dst == {vpn_ip}\" -w \"{outgoing_pcap}\""
    # Command for filtering incoming packets (VPN to Alexa)
    incoming_command = f"tshark -r \"{pcap_file}\" -Y \"ip.src == {vpn_ip} and ip.dst == {alexa_ip}\" -w \"{incoming_pcap}\""

    subprocess.run(outgoing_command, shell=True)
    subprocess.run(incoming_command, shell=True)

    print(f"Filtered outgoing traffic saved to {outgoing_pcap}")
    print(f"Filtered incoming traffic saved to {incoming_pcap}")

def main():
    parser = argparse.ArgumentParser(description='Filter network traffic between Alexa and VPN server into separate directories.')
    parser.add_argument('--raw_dir', type=str, required=True, help='Directory containing raw traffic data (.pcap files)')
    parser.add_argument('--outgoing_dir', type=str, required=True, help='Directory to save filtered outgoing traffic data')
    parser.add_argument('--incoming_dir', type=str, required=True, help='Directory to save filtered incoming traffic data')
    parser.add_argument('--alexa_ip', type=str, required=True, help='IP address of the Alexa device')
    parser.add_argument('--vpn_ip', type=str, required=True, help='IP address of the VPN server')
    args = parser.parse_args()

    pcap_files = [f for f in os.listdir(args.raw_dir) if f.endswith('.pcap')]
    for pcap_file in pcap_files:
        full_pcap_path = os.path.join(args.raw_dir, pcap_file)
        filter_and_save_traffic(full_pcap_path, args.alexa_ip, args.vpn_ip, args.outgoing_dir, args.incoming_dir)

if __name__ == "__main__":
    main()


# python traffic_filter.py --raw_dir "ground_truth/traffic_W" --outgoing_dir "ground_truth/traffic_W_outgoing" --incoming_dir "ground_truth/traffic_W_incoming" --alexa_ip "10.0.0.159" --vpn_ip "81.181.57.28"
