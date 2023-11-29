from scapy.all import rdpcap, IP, TCP, UDP

def analyze_pcap(file_path):
    try:
        packets = rdpcap(file_path)
        for packet in packets:
            if IP in packet:
                timestamp = packet.time
                source_ip = packet[IP].src
                dest_ip = packet[IP].dst
                packet_size = len(packet)

                protocol = None
                if TCP in packet:
                    protocol = "TCP"
                elif UDP in packet:
                    protocol = "UDP"
                
                # info = packet.summary()

                print(f"Timestamp: {timestamp}, Source: {source_ip}, Destination: {dest_ip}, Packet Size: {packet_size}, Protocol: {protocol}")
    except Exception as e:
        print(f"Error analyzing pcap file: {e}")

def main():
    pcap_file_path = 'traffic_capture.pcap'
    analyze_pcap(pcap_file_path)

if __name__ == "__main__":
    main()
