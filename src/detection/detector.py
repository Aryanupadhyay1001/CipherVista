from src.detection.rules import RuleEngine
from src.detection.alert_manager import AlertManager
from src.detection.correlator import DetectionCorrelator
from src.ml.realtime.flow_manager import FlowManager
from src.ml.realtime.ml_detector import MLDetector
from scapy.layers.inet import IP
from src.ml.realtime.prediction_manager import PredictionManager
from src.ai.soc_analyst import SOCAnalyst
from src.ai.analysis_queue import AnalysisQueue
from src.ai.batch_soc_analyst import BatchSOCAnalyst
from src.detection.incident_manager import IncidentManager

import time

class ThreatDetector:

    def __init__(self):

        self.rule_engine = RuleEngine()

        self.flow_manager = FlowManager()

        self.ml_detector = MLDetector()

        self.prediction_manager = PredictionManager()

        self.batch_soc_analyst = BatchSOCAnalyst()

        self.last_batch_time = time.time()

        self.analysis_queue = AnalysisQueue()

        self.correlator = DetectionCorrelator()

        self.incident_manager = IncidentManager()

        self.alert_manager = AlertManager()

    def process_packet(self, packet):

        if not packet.haslayer(IP):
            return

        rule_threats = self.rule_engine.analyze(packet)

        for threat in rule_threats:

            threat = self.incident_manager.process(threat)

            if threat:

                self.alert_manager.add_alert(threat)

                self.analysis_queue.add(threat)

        self.flow_manager.process_packet(packet)

        ready_flows = self.flow_manager.get_ready_flows()

        for flow in ready_flows:

            ml_prediction = self.ml_detector.detect(flow)

            self.prediction_manager.add({

                "time": time.strftime("%H:%M:%S"),
                "source": flow.src_ip,
                "destination": flow.dst_ip,
                "protocol": flow.protocol,
                "prediction": ml_prediction["attack"],
                "confidence": ml_prediction["confidence"],
                "anomaly": ml_prediction["is_anomaly"],
                "anomaly_score": ml_prediction["anomaly_score"]

            })

            threat = self.correlator.correlate(
                rule_threats,
                ml_prediction,
                flow
            )

            if threat:

                threat = self.incident_manager.process(threat)

                if threat:

                    self.alert_manager.add_alert(threat)

                    self.analysis_queue.add(threat)

        self.process_ai_queue()

        self.flow_manager.get_completed_flows()

    def get_alerts(self):

        return self.alert_manager.get_alerts()

    def clear_alerts(self):

        self.alert_manager.clear_alerts()

    def get_statistics(self):

        return {

            "total": self.alert_manager.total_alerts(),

            "critical": self.alert_manager.critical_alerts(),

            "high": self.alert_manager.high_alerts(),

            "medium": self.alert_manager.medium_alerts(),

            "low": self.alert_manager.low_alerts()
        }

    def get_predictions(self):

        return self.prediction_manager.get_predictions()

    def reset(self):

        self.rule_engine.reset()

        self.flow_manager.clear()

        self.alert_manager.reset()

        self.prediction_manager.clear()

        self.batch_soc_analyst.clear()

        self.analysis_queue.clear()

    def get_ai_analyses(self):

        return self.batch_soc_analyst.get_analyses()

    def get_analysis_queue(self):

        return self.analysis_queue

    def process_ai_queue(self):

        queue = self.analysis_queue.get_all()

        current_time = time.time()

        if not queue:
            return

        if len(queue) >= 10 or current_time - self.last_batch_time >= 30:

            self.batch_soc_analyst.analyze(queue)

            self.analysis_queue.clear()

            self.last_batch_time = current_time
        else:

            return