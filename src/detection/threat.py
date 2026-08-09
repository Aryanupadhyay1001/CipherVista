from dataclasses import dataclass


@dataclass
class Threat:

    time: str

    source_ip: str

    destination_ip: str

    protocol: str

    threat_type: str

    severity: str

    risk_score: int

    confidence: int

    description: str

    evidence: list

    detection: str

    mitre: str