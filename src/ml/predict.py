import numpy as np
import pandas as pd


class ThreatPredictor:

    def __init__(self,
                 anomaly_model,
                 classifier_model):

        self.anomaly_model = anomaly_model
        self.classifier_model = classifier_model

    def predict_dataframe(self, df):

        X = df.copy()

        if "Label" in X.columns:
            X = X.drop("Label", axis=1)

        anomaly_prediction = self.anomaly_model.predict(X)

        anomaly_score = self.anomaly_model.decision_function(X)

        attack_prediction = self.classifier_model.predict(X)

        print("Unique raw predictions:", np.unique(attack_prediction))
        print("Prediction dtype:", attack_prediction.dtype)

        confidence = self.classifier_model.predict_proba(X).max(axis=1)

        result = pd.DataFrame()

        result["anomaly"] = anomaly_prediction == -1

        result["anomaly_score"] = anomaly_score

        result["prediction"] = np.where(
            attack_prediction == 1,
            "Attack",
            "Benign"
        )

        result["confidence"] = confidence * 100

        print(result["prediction"].value_counts())

        return result