from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP, ICMP
import threading
import time
from src.detection.detector import ThreatDetector

class PacketCapture:

    def __init__(self):

        self.running = False
        self.thread = None
        self.lock = threading.Lock()

        self.packet_count = 0
        self.tcp_count = 0
        self.udp_count = 0
        self.icmp_count = 0

        self.start_time = None
        self.interface = "None"

        self.recent_packets = []
        self.detector = ThreatDetector()

    def process_packet(self, packet):

        try:

            if not packet.haslayer(IP):
                return

            self.packet_count += 1

            protocol = "OTHER"

            if packet.haslayer(TCP):
                self.tcp_count += 1
                protocol = "TCP"

            elif packet.haslayer(UDP):
                self.udp_count += 1
                protocol = "UDP"

            elif packet.haslayer(ICMP):
                self.icmp_count += 1
                protocol = "ICMP"

            src_ip = "-"
            dst_ip = "-"

            if packet.haslayer(IP):
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst

            self.recent_packets.append({
                "time": time.strftime("%H:%M:%S"),
                "src": src_ip,
                "dst": dst_ip,
                "protocol": protocol,
                "length": len(packet)
            })

            if len(self.recent_packets) > 100:
                self.recent_packets.pop(0)

            self.detector.process_packet(packet)

        except Exception:
            return

    def capture_loop(self, interface):

        sniff(
            iface=interface,
            prn=self.process_packet,
            store=False,
            stop_filter=lambda x: not self.running
        )

    def start_capture(self, interface):

        if self.running:
            self.stop_capture()

        with self.lock:
            self.reset_statistics()

        self.detector.reset()

        self.running = True
        self.interface = interface

        self.thread = threading.Thread(
            target=self.capture_loop,
            args=(interface,),
            daemon=True
        )

        self.thread.start()

    def stop_capture(self):

        self.running = False

    def packets_per_second(self):

        if self.start_time is None:
            return 0

        elapsed = time.time() - self.start_time

        if elapsed == 0:
            return 0

        return round(
            self.packet_count / elapsed,
            2
        )

    def get_statistics(self):

        return {
            "total_packets": self.packet_count,
            "tcp_packets": self.tcp_count,
            "udp_packets": self.udp_count,
            "icmp_packets": self.icmp_count,
            "packets_per_second": self.packets_per_second(),
            "running": self.running,
            "interface": self.interface
        }

    def get_recent_packets(self):

        with self.lock:
            return list(self.recent_packets)

    def reset_statistics(self):

        self.packet_count = 0
        self.tcp_count = 0
        self.udp_count = 0
        self.icmp_count = 0

        self.recent_packets.clear()

        self.start_time = time.time()

    def get_alerts(self):

        return self.detector.get_alerts()

    def get_predictions(self):

        return self.detector.get_predictions()

    def get_ai_analyses(self):

        return self.detector.get_ai_analyses()

    def get_alert_statistics(self):

        return self.detector.get_statistics()