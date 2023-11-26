from scapy.all import *
import time

def start_traffic_detection(interface, monitor_ip):
    # Initialize variables
    last_check = time.time()
    packet_count = 0

    def detect_traffic(packet):
        nonlocal last_check, packet_count

        # Check if the packet is related to the specified IP
        if is_target_packet(packet):
            packet_count += 1

            current_time = time.time()
            elapsed_time = current_time - last_check

            # Check if one second has passed
            if elapsed_time >= 1:
                # Calculate packets per second for the specified IP traffic
                pps = packet_count / elapsed_time
                print(f"Traffic for IP {monitor_ip}: {pps} packets per second")

                # Reset counters
                last_check = current_time
                packet_count = 0

    def is_target_packet(packet):
        """
        Checks if the given packet is related to the specified IP address.
        """

        # Check if the packet has an IP layer
        if packet.haslayer(IP):
            ip_src = packet.getlayer(IP).src
            ip_dst = packet.getlayer(IP).dst

            # Check if the packet's source or destination IP is the target IP
            if ip_src == monitor_ip or ip_dst == monitor_ip:
                return True

        return False

    # Start sniffing on the specified interface
    sniff(iface=interface, prn=detect_traffic)
