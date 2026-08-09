from collections import defaultdict
import time

from scapy.layers.inet import IP, TCP, UDP, ICMP

from src.detection.threat import Threat

class RuleEngine:

    def __init__(self):

        self.syn_tracker = defaultdict(list)
        self.port_tracker = defaultdict(set)
        self.icmp_tracker = defaultdict(list)
        self.udp_tracker = defaultdict(list)
        self.last_icmp_alert = {}
        self.last_udp_alert = {}
        self.last_syn_alert = {}

    def analyze(self, packet):

        threats = []

        current_time = time.time()

        if not packet.haslayer(IP):
            return threats

        src = packet[IP].src
        dst = packet[IP].dst

        # --------------------------
        # ICMP Flood
        # --------------------------

        if packet.haslayer(ICMP):

            if packet[ICMP].type != 8:
                return threats

            self.icmp_tracker[src].append(current_time)

            self.icmp_tracker[src] = [
                t for t in self.icmp_tracker[src]
                if current_time - t <= 5
            ]

            if len(self.icmp_tracker[src]) > 5:

                last = self.last_icmp_alert.get(src, 0)

                if current_time - last > 0:

                    self.last_icmp_alert[src] = current_time

                    threats.append(

                        Threat(

                            time=time.strftime("%H:%M:%S"),

                            source_ip=src,

                            destination_ip=dst,

                            protocol="ICMP",

                            threat_type="ICMP Flood",

                            severity="Critical",

                            risk_score=95,

                            confidence=98,

                            description="Excessive ICMP packets detected.",

                            evidence=[
                                f"ICMP packets: {len(self.icmp_tracker[src])}"
                            ],

                            detection="Rule Engine",

                            mitre="T1498"
                        )
                    )

        # --------------------------
        # UDP Flood
        # --------------------------

        if packet.haslayer(UDP):

            self.udp_tracker[src].append(current_time)

            self.udp_tracker[src] = [
                t for t in self.udp_tracker[src]
                if current_time - t <= 5
            ]

            if len(self.udp_tracker[src]) > 20:

                threats.append(
                    Threat(

                    time=time.strftime("%H:%M:%S"),

                    source_ip=src,

                    destination_ip=dst,

                    protocol="UDP",

                    threat_type="UDP Flood",

                    severity="High",

                    risk_score=85,

                    confidence=92,

                    description="Excessive UDP packets detected.",

                    evidence=[
                        f"UDP packets: {len(self.udp_tracker[src])}",
                        "Exceeded UDP flood threshold"
                    ],

                    detection="Rule Engine",

                    mitre="T1498"
                )
                )

        # --------------------------
        # SYN Flood
        # --------------------------

        if packet.haslayer(TCP):

            flags = packet[TCP].flags

            if flags == "S":

                self.syn_tracker[src].append(current_time)

                self.syn_tracker[src] = [
                    t for t in self.syn_tracker[src]
                    if current_time - t <= 5
                ]

                if len(self.syn_tracker[src]) > 15:

                    threats.append(
                        Threat(

                        time=time.strftime("%H:%M:%S"),

                        source_ip=src,

                        destination_ip=dst,

                        protocol="TCP",

                        threat_type="SYN Flood",

                        severity="Critical",

                        risk_score=97,

                        confidence=99,

                        description="Possible SYN flood attack detected.",

                        evidence=[
                            f"SYN packets: {len(self.syn_tracker[src])}",
                            "Large number of SYN packets observed"
                        ],

                        detection="Rule Engine",

                        mitre="T1498"
                    )
                    )

                self.port_tracker[src].add(packet[TCP].dport)

                if len(self.port_tracker[src]) > 6:

                    threats.append(
                        Threat(
                            time=time.strftime("%H:%M:%S"),
                            source_ip=src,
                            destination_ip=dst,
                            protocol="TCP",
                            threat_type="Port Scan",
                            severity="High",
                            risk_score=95,
                            confidence=95,
                            description="Multiple destination ports contacted.",
                            evidence=["Rule Engine"],
                            detection="Rule Engine",
                            mitre="T1046"
                        )
                    )

        return threats

    def reset(self):

        self.syn_tracker.clear()
        self.port_tracker.clear()
        self.icmp_tracker.clear()
        self.udp_tracker.clear()