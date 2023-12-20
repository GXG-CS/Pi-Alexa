from scapy.all import rdpcap, IP
import matplotlib.pyplot as plt
import argparse
from datetime import datetime

ALEXA_IP = '10.3.141.158'
AMAZON_SERVER_IPS = ['44.199.80.228', '3.223.181.245', '54.167.177.211']  # Example list of server IPs

def analyze_traffic(pcap_file):
    packets = rdpcap(pcap_file)
    print(f"Total number of packets in the pcap file: {len(packets)}")

    timestamps_incoming = []
    timestamps_outgoing = []
    sizes_incoming = []
    sizes_outgoing = []

    for packet in packets:
        if IP in packet:
            packet_time = datetime.fromtimestamp(float(packet.time))
            packet_size = len(packet) * 8 / 1024  # Convert bytes to Kilobits

            if packet[IP].src == ALEXA_IP and packet[IP].dst in AMAZON_SERVER_IPS:
                timestamps_outgoing.append(packet_time.timestamp())
                sizes_outgoing.append(packet_size)
            elif packet[IP].src in AMAZON_SERVER_IPS and packet[IP].dst == ALEXA_IP:
                timestamps_incoming.append(packet_time.timestamp())
                sizes_incoming.append(packet_size)

    return timestamps_incoming, sizes_incoming, timestamps_outgoing, sizes_outgoing

def aggregate_traffic(timestamps, sizes):
    start_time = min(timestamps)
    end_time = max(timestamps)
    interval = 1  # Aggregate data in 1-second intervals
    rates = []

    for i in range(int(start_time), int(end_time) + 1, interval):
        bytes_in_interval = sum(size for time, size in zip(timestamps, sizes) if i <= time < i + interval)
        rates.append(bytes_in_interval)  # Traffic rate in Kilobits per second

    return rates

def plot_traffic_curve(incoming_rates, outgoing_rates):
    plt.figure(figsize=(12, 6))
    plt.plot(incoming_rates, label='Incoming', marker='x')
    plt.plot(outgoing_rates, label='Outgoing', marker='o')
    plt.xlabel('Time (s)')
    plt.ylabel('Traffic Rate (Kb/s)')
    plt.title('Traffic Rate over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig('traffic_rate_plot7.png', dpi=300)
    print("Plot saved as traffic_rate_plot7.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze a pcap file and plot traffic rates for Alexa and Amazon server.')
    parser.add_argument('pcap_file', type=str, help='The path to the pcap file to analyze')

    args = parser.parse_args()

    print("Starting traffic analysis...")
    timestamps_incoming, sizes_incoming, timestamps_outgoing, sizes_outgoing = analyze_traffic(args.pcap_file)

    print(f"Incoming packets: {len(timestamps_incoming)}")
    print(f"Outgoing packets: {len(timestamps_outgoing)}")

    if timestamps_incoming and timestamps_outgoing:
        print("Aggregating traffic rates...")
        incoming_rates = aggregate_traffic(timestamps_incoming, sizes_incoming)
        outgoing_rates = aggregate_traffic(timestamps_outgoing, sizes_outgoing)

        print("Plotting traffic rates...")
        plot_traffic_curve(incoming_rates, outgoing_rates)
    else:
        print("No traffic found for the specified IP addresses.")


# python traffic_analysis.py traffic_W/test2.pcap 