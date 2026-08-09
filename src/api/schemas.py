from pydantic import BaseModel
from typing import List


class PredictionRequest(BaseModel):
    features: List[float]


class PredictionResponse(BaseModel):
    anomaly: bool
    anomaly_score: float
    attack_type: str
    confidence: float
    severity: str

    