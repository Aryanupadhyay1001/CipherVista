import joblib
import pandas as pd

from src.ml.feature_schema import FEATURE_COLUMNS


class ModelManager:

    def __init__(self):

        self.random_forest = joblib.load(
            "models/random_forest.pkl"
        )

        self.isolation_forest = joblib.load(
            "models/isolation_forest.pkl"
        )

        self.scaler = joblib.load(
            "models/scaler.pkl"
        )

        self.label_encoder = joblib.load(
            "models/label_encoder.pkl"
        )

    def prepare(self, features_df):

        features_df = features_df.copy()

        missing = [
            column
            for column in FEATURE_COLUMNS
            if column not in features_df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing features: {missing}"
            )

        features_df = features_df[FEATURE_COLUMNS]

        scaled = self.scaler.transform(
            features_df
        )

        scaled = pd.DataFrame(
            scaled,
            columns=FEATURE_COLUMNS
        )

        return scaled

    def predict(self, features_df):

        scaled = self.prepare(
            features_df
        )
        print("RF Predict")
        rf_prediction = self.random_forest.predict(
            scaled
        )[0]

        print("RF Probability")
        rf_probability = max(
            self.random_forest.predict_proba(
                scaled
            )[0]
        )

        attack_name = self.label_encoder.inverse_transform(
            [rf_prediction]
        )[0]
        print("Isolation Predict")
        anomaly = self.isolation_forest.predict(
            scaled
        )[0]
        print("Isolation Score")
        anomaly_score = self.isolation_forest.decision_function(
            scaled
        )[0]

        is_anomaly = (
            anomaly == -1
            and anomaly_score < -0.10
        )

        print(
            f"Isolation Prediction={anomaly}, "
            f"Score={anomaly_score:.4f}, "
            f"Alert={is_anomaly}"
        )

        return {

            "attack": attack_name,

            "confidence": round(
                rf_probability * 100,
                2
            ),

            "is_anomaly": is_anomaly,

            "anomaly_score": round(
                anomaly_score,
                4
            )
        }