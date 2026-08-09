import time

from src.ml.realtime.flow import Flow
from scapy.layers.inet import IP
from scapy.layers.inet import IP, TCP, UDP


class FlowManager:

    def __init__(self):

        self.flows = {}

        self.completed_flows = []

        self.timeout = 1

    def flow_key(self, packet):

        if not packet.haslayer(IP):
            return None

        src_ip = packet["IP"].src
        dst_ip = packet["IP"].dst

        protocol = packet["IP"].proto

        if packet.haslayer("TCP"):

            src_port = packet["TCP"].sport
            dst_port = packet["TCP"].dport

        elif packet.haslayer("UDP"):

            src_port = packet["UDP"].sport
            dst_port = packet["UDP"].dport

        else:

            src_port = 0
            dst_port = 0

        return (
            src_ip,
            dst_ip,
            src_port,
            dst_port,
            protocol
        )

    def process_packet(self, packet):

        key = self.flow_key(packet)

        if key is None:
            return

        if key not in self.flows:

            self.flows[key] = Flow(packet)

        else:

            self.flows[key].update(packet)

    def get_completed_flows(self):

        now = time.time()

        expired = []

        for key, flow in list(self.flows.items()):

            if now - flow.last_seen > self.timeout:

                expired.append(flow)

                del self.flows[key]

        return expired

    def get_ready_flows(self):

        ready = []

        for flow in self.flows.values():

            if flow.packet_count >= 20:

                ready.append(flow)

                flow.packet_count = 0

        return ready

    def active_flow_count(self):

        return len(self.flows)

    def clear(self):

        self.flows.clear()

        self.completed_flows.clear()