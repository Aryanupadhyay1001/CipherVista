import time

from src.detection.threat import Threat
from src.detection.severity import SeverityCalculator
from src.detection.mitre_mapper import get_mitre


class DetectionCorrelator:

    def __init__(self):

        self.severity_calculator = SeverityCalculator()

    def correlate(
        self,
        rule_threats,
        ml_prediction,
        flow
    ):

        severity_info = self.severity_calculator.calculate(
            rule_threats,
            ml_prediction,
            flow
        )

        evidence = []

        if rule_threats:
            evidence.append("Rule Engine")

        if ml_prediction["attack"] != "Benign":
            evidence.append("Random Forest")

        if ml_prediction["is_anomaly"]:
            evidence.append("Isolation Forest")

        if (
            ml_prediction["attack"] == "Benign"
            and not ml_prediction["is_anomaly"]
        ):
            return None

        if ml_prediction["attack"] != "Benign":
            threat_type = ml_prediction["attack"]

        elif rule_threats:
            threat_type = rule_threats[0].threat_type

        else:
            threat_type = "Anomalous Traffic"

        description = ""

        if rule_threats:
            description += rule_threats[0].description

        if ml_prediction["attack"] != "Benign":
            if description:
                description += "\n"
            description += f"ML Prediction: {ml_prediction['attack']}"

        if ml_prediction["is_anomaly"]:
            if description:
                description += "\n"
            description += "Isolation Forest detected anomalous behaviour."

        mitre = get_mitre(threat_type)

        if rule_threats and (
            ml_prediction["attack"] != "Benign"
            or ml_prediction["is_anomaly"]
        ):
            detection = "Rule + ML"

        elif rule_threats:
            detection = "Rule Engine"

        else:
            detection = "ML Engine"

        return Threat(

            time=time.strftime("%H:%M:%S"),

            source_ip=flow.src_ip,

            destination_ip=flow.dst_ip,

            protocol=str(flow.protocol),

            threat_type=threat_type,

            severity=severity_info["severity"],

            risk_score=severity_info["score"],

            confidence=int(ml_prediction["confidence"]),

            description=description,

            evidence=evidence,

            detection=detection,
            mitre=get_mitre(threat_type)["id"]
        )