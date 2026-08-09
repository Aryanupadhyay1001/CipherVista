import time
import numpy as np

from scapy.layers.inet import IP, TCP
from scapy.layers.inet import IP


class Flow:

    def __init__(self, packet):

        self.packet_count = 1

        self.start_time = time.time()
        self.last_seen = self.start_time

        ip = packet[IP]

        self.src_ip = ip.src
        self.dst_ip = ip.dst

        self.protocol = ip.proto

        if packet.haslayer(TCP):

            tcp = packet[TCP]

            self.src_port = tcp.sport
            self.dst_port = tcp.dport

        else:

            self.src_port = 0
            self.dst_port = 0

        self.total_packets = 0
        self.total_bytes = 0

        self.forward_packets = 0
        self.backward_packets = 0

        self.forward_bytes = 0
        self.backward_bytes = 0

        self.packet_lengths = []

        self.syn_count = 0
        self.ack_count = 0
        self.fin_count = 0
        self.rst_count = 0

        self.inter_arrival_times = []

        self.update(packet)

    def update(self, packet):

        self.packet_count += 1

        now = time.time()

        self.inter_arrival_times.append(
            now - self.last_seen
        )

        self.last_seen = now

        length = len(packet)

        self.total_packets += 1
        self.total_bytes += length

        self.packet_lengths.append(length)

        if packet[IP].src == self.src_ip:

            self.forward_packets += 1
            self.forward_bytes += length

        else:

            self.backward_packets += 1
            self.backward_bytes += length

        if packet.haslayer(TCP):

            flags = packet[TCP].flags

            if flags & 0x02:
                self.syn_count += 1

            if flags & 0x10:
                self.ack_count += 1

            if flags & 0x01:
                self.fin_count += 1

            if flags & 0x04:
                self.rst_count += 1

    def duration(self):

        return self.last_seen - self.start_time

    def packets_per_second(self):

        duration = self.duration()

        if duration <= 0:
            return 0

        return self.total_packets / duration

    def bytes_per_second(self):

        duration = self.duration()

        if duration <= 0:
            return 0

        return self.total_bytes / duration


    def flow_iat_mean(self):

        if len(self.inter_arrival_times) == 0:
            return 0

        return float(
            np.mean(self.inter_arrival_times)
        )


    def flow_iat_std(self):

        if len(self.inter_arrival_times) == 0:
            return 0

        return float(
            np.std(self.inter_arrival_times)
        )