from src.ml.realtime.feature_generator import FeatureGenerator
from src.ml.model_manager import ModelManager

class MLDetector:

    def __init__(self):
        self.model_manager = ModelManager()

    def detect(self, flow):
        features = FeatureGenerator.generate(flow)

        prediction = self.model_manager.predict(
            features
        )

        return prediction