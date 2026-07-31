import joblib
import numpy as np
import pandas as pd


class ThreatPredictor:

    def __init__(
        self,
        anomaly_model,
        classifier_model
    ):

        self.anomaly_model = anomaly_model
        self.classifier_model = classifier_model

        self.label_encoder = joblib.load(
            "models/label_encoder.pkl"
        )

    def predict_dataframe(self, df):

        X = df.copy()

        if "Label" in X.columns:
            X = X.drop("Label", axis=1)

        anomaly_prediction = self.anomaly_model.predict(X)

        anomaly_score = self.anomaly_model.decision_function(X)

        attack_prediction = self.classifier_model.predict(X)

        attack_names = self.label_encoder.inverse_transform(
            attack_prediction
        )

        confidence = (
            self.classifier_model
            .predict_proba(X)
            .max(axis=1)
        )

        result = pd.DataFrame()

        result["anomaly"] = (
            anomaly_prediction == -1
        )

        result["anomaly_score"] = anomaly_score

        result["prediction"] = attack_names

        result["confidence"] = (
            confidence * 100
        ).round(2)

        attack_breakdown = (
            result[
                result["prediction"] != "Benign"
            ]["prediction"]
            .value_counts()
            .to_dict()
        )

        result.attrs["attack_breakdown"] = attack_breakdown

        return result