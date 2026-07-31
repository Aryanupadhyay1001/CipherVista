import os
import logging
import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class ModelTrainer:

    def __init__(self, data_path, model_path):

        self.data_path = data_path
        self.model_path = model_path

        self.data = None
        self.model = None

    def load_data(self):

        logger.info("Loading feature dataset...")

        self.data = pd.read_pickle(self.data_path)

        logger.info(
            f"Dataset loaded ({self.data.shape[0]} rows)."
        )

    def train(self):

        logger.info("Training Isolation Forest...")

        X = self.data.drop("Label", axis=1)

        self.model = IsolationForest(
            n_estimators=200,
            contamination=0.02,
            random_state=42,
            n_jobs=-1,
            verbose=1
        )

        self.model.fit(X)

        logger.info("Training completed.")

    def evaluate(self):

        logger.info("Evaluating model...")

        X = self.data.drop("Label", axis=1)

        y_true = self.data["Label"]

        predictions = self.model.predict(X)

        y_pred = [0 if x == 1 else 1 for x in predictions]

        logger.info("")
        logger.info("========== MODEL PERFORMANCE ==========")

        logger.info(
            f"Accuracy  : {accuracy_score(y_true, y_pred):.4f}"
        )

        logger.info(
            f"Precision : {precision_score(y_true, y_pred):.4f}"
        )

        logger.info(
            f"Recall    : {recall_score(y_true, y_pred):.4f}"
        )

        logger.info(
            f"F1 Score  : {f1_score(y_true, y_pred):.4f}"
        )

        logger.info("")
        logger.info("Confusion Matrix")
        logger.info("\n%s", confusion_matrix(y_true, y_pred))

        logger.info("")
        logger.info("Classification Report")
        logger.info(
            "\n%s",
            classification_report(y_true, y_pred)
        )

        logger.info("=======================================")

    def save_model(self):

        os.makedirs(
            os.path.dirname(self.model_path),
            exist_ok=True
        )

        joblib.dump(
            self.model,
            self.model_path
        )

        logger.info(
            f"Model saved to {self.model_path}"
        )

    def run(self):

        self.load_data()

        self.train()

        self.evaluate()

        self.save_model()


if __name__ == "__main__":

    trainer = ModelTrainer(
    data_path="data/processed/final_dataset.pkl",
    model_path="models/isolation_forest.pkl"
)

    trainer.run()