from scapy.all import rdpcap, Ether
import matplotlib.pyplot as plt
import argparse
import datetime

def analyze_traffic(pcap_file, device_mac):
    packets = rdpcap(pcap_file)
    timestamps_incoming = []
    timestamps_outgoing = []
    sizes_incoming = []
    sizes_outgoing = []

    for packet in packets:
        if Ether in packet:
            packet_time = datetime.datetime.fromtimestamp(packet.time)
            packet_size = len(packet) * 8 / 1024  # Convert bytes to Kilobits

            # Check if the packet is incoming or outgoing based on MAC address
            if packet[Ether].dst.lower() == device_mac.lower():
                timestamps_incoming.append(packet_time.timestamp())
                sizes_incoming.append(packet_size)
            elif packet[Ether].src.lower() == device_mac.lower():
                timestamps_outgoing.append(packet_time.timestamp())
                sizes_outgoing.append(packet_size)

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
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze a pcap file and plot traffic rates for a given MAC address.')
    parser.add_argument('pcap_file', type=str, help='The path to the pcap file to analyze')
    parser.add_argument('device_mac', type=str, help='The MAC address of the Alexa device')

    args = parser.parse_args()

    timestamps_incoming, sizes_incoming, timestamps_outgoing, sizes_outgoing = analyze_traffic(args.pcap_file, args.device_mac)

    if timestamps_incoming and timestamps_outgoing:
        incoming_rates = aggregate_traffic(timestamps_incoming, sizes_incoming)
        outgoing_rates = aggregate_traffic(timestamps_outgoing, sizes_outgoing)
        plot_traffic_curve(incoming_rates, outgoing_rates)
    else:
        print("No traffic found for the specified MAC address.")

#  python traffic_analysis.py traffic_W/test2.pcap 