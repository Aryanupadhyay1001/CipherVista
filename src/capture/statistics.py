import time
from scapy.layers.inet import IP, TCP, UDP, ICMP


class StatisticsEngine:

    def __init__(self):

        self.total_packets = 0
        self.tcp_packets = 0
        self.udp_packets = 0
        self.icmp_packets = 0

        self.start_time = time.time()

        self.recent_packets = []

    def process_packet(self, packet):

        self.total_packets += 1

        protocol = "OTHER"

        if packet.haslayer(TCP):
            self.tcp_packets += 1
            protocol = "TCP"

        elif packet.haslayer(UDP):
            self.udp_packets += 1
            protocol = "UDP"

        elif packet.haslayer(ICMP):
            self.icmp_packets += 1
            protocol = "ICMP"

        src = "-"
        dst = "-"

        if packet.haslayer(IP):
            src = packet[IP].src
            dst = packet[IP].dst

        self.recent_packets.append(
            {
                "Time": time.strftime("%H:%M:%S"),
                "Source": src,
                "Destination": dst,
                "Protocol": protocol,
                "Length": len(packet)
            }
        )

        if len(self.recent_packets) > 200:
            self.recent_packets.pop(0)

    def packets_per_second(self):

        elapsed = time.time() - self.start_time

        if elapsed <= 0:
            return 0

        return round(
            self.total_packets / elapsed,
            2
        )

    def get_statistics(self):

        return {

            "total_packets": self.total_packets,

            "tcp_packets": self.tcp_packets,

            "udp_packets": self.udp_packets,

            "icmp_packets": self.icmp_packets,

            "packets_per_second": self.packets_per_second()
        }

    def get_recent_packets(self):

        return self.recent_packets