import numpy as np
import pandas as pd


class FeatureGenerator:

    @staticmethod
    def generate(flow):

        duration = flow.duration()

        if duration <= 0:
            duration = 1e-6

        packet_lengths = flow.packet_lengths

        features = {

        "Flow Duration": duration,

        "Total Fwd Packets": flow.forward_packets,

        "Total Backward Packets": flow.backward_packets,

        "Total Length of Fwd Packets": flow.forward_bytes,

        "Total Length of Bwd Packets": flow.backward_bytes,

        "Flow Bytes/s": flow.total_bytes / duration,

        "Flow Packets/s": flow.total_packets / duration,

        "Packet Length Mean": np.mean(packet_lengths),

        "Packet Length Std": np.std(packet_lengths),

        "Average Packet Size": np.mean(packet_lengths),

        "Flow IAT Mean": flow.flow_iat_mean(),

        "Flow IAT Std": flow.flow_iat_std(),

        "SYN Flag Count": flow.syn_count,

        "ACK Flag Count": flow.ack_count,

        "FIN Flag Count": flow.fin_count,

        "RST Flag Count": flow.rst_count,

        "Fwd Packets/s": flow.forward_packets / duration,

        "Bwd Packets/s": flow.backward_packets / duration,

        "Protocol": flow.protocol,

        "Source Port": flow.src_port,

        "Destination Port": flow.dst_port
    }

        return pd.DataFrame([features])