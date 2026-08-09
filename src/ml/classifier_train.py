import os
import logging
import joblib
import pandas as pd
import numpy as np

from src.ml.feature_schema import FEATURE_COLUMNS

from sklearn.preprocessing import (
    LabelEncoder,
    StandardScaler
)

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class ClassifierTrainer:

    def __init__(self, data_path, model_path):

        self.data_path = data_path
        self.model_path = model_path

        self.data = None
        self.model = None

        self.scaler = None
        self.label_encoder = None

    def load_data(self):

        logger.info("Loading feature dataset in chunks...")

        chunks = []

        chunk_size = 100000
        sample_fraction = 0.18

        for i, chunk in enumerate(
            pd.read_csv(
                self.data_path,
                chunksize=chunk_size,
                low_memory=False
            )
        ):

            sampled_chunk = chunk.sample(
                frac=sample_fraction,
                random_state=42
            )

            chunks.append(sampled_chunk)

            logger.info(
                f"Processed chunk {i+1}"
            )

        self.data = pd.concat(
            chunks,
            ignore_index=True
        )

        logger.info(
            f"Sampled Dataset : {self.data.shape[0]} rows"
        )

    def split_data(self):

        logger.info("Preparing training data...")

        columns_to_drop = [
            "Flow ID",
            "Source IP",
            "Destination IP",
            "Timestamp"
        ]

        self.data.drop(
            columns=[c for c in columns_to_drop if c in self.data.columns],
            inplace=True
        )

        self.label_encoder = LabelEncoder()

        self.data["Label"] = self.label_encoder.fit_transform(
            self.data["Label"]
        )

        os.makedirs(
            "models",
            exist_ok=True
        )

        joblib.dump(
            self.label_encoder,
            "models/label_encoder.pkl"
        )

        

        missing = [
            column
            for column in FEATURE_COLUMNS
            if column not in self.data.columns
        ]

        if missing:

            raise ValueError(
                f"Missing required features: {missing}"
            )

        X = self.data[FEATURE_COLUMNS]

        y = self.data["Label"]

        X = X.replace([np.inf, -np.inf], np.nan)

        X = X.apply(
            pd.to_numeric,
            errors="coerce"
        )

        X = X.fillna(
            X.median()
        )

        self.scaler = StandardScaler()

        self.feature_names = X.columns.tolist()

        X = self.scaler.fit_transform(X)

        joblib.dump(
            self.scaler,
            "models/scaler.pkl"
        )

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        logger.info(
            f"Training samples : {len(self.X_train)}"
        )

        logger.info(
            f"Testing samples : {len(self.X_test)}"
        )

        logger.info(
            f"Classes : {list(self.label_encoder.classes_)}"
        )

    def train(self):

        logger.info("Training Random Forest...")

        self.model = RandomForestClassifier(
            n_estimators=300,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
            verbose=0
        )

        self.model.fit(
            self.X_train,
            self.y_train
        )

        logger.info("Training completed.")

    def evaluate(self):

        logger.info("Evaluating model...")

        predictions = self.model.predict(
            self.X_test
        )

        logger.info("")
        logger.info("========== MODEL PERFORMANCE ==========")

        logger.info(
            f"Accuracy  : {accuracy_score(self.y_test, predictions):.4f}"
        )

        logger.info(
            f"Precision : {precision_score(
    self.y_test,
    predictions,
    average="weighted",
    zero_division=0
):.4f}"
        )

        logger.info(
            f"Recall    : {recall_score(
    self.y_test,
    predictions,
    average="weighted",
    zero_division=0
):.4f}"
        )

        logger.info(
            f"F1 Score  : {f1_score(
    self.y_test,
    predictions,
    average="weighted",
    zero_division=0
):.4f}"
        )

        logger.info("")
        logger.info("Confusion Matrix")

        logger.info(
            "\n%s",
            confusion_matrix(self.y_test, predictions)
        )

        logger.info("")
        logger.info("Classification Report")

        logger.info(
            "\n%s",
            classification_report(
    self.y_test,
    predictions,
    labels=range(len(self.label_encoder.classes_)),
    target_names=self.label_encoder.classes_,
    zero_division=0
)
        )

    def feature_importance(self):

        importance = pd.DataFrame({
    "Feature": self.feature_names,
    "Importance": self.model.feature_importances_
})

        importance = importance.sort_values(
            by="Importance",
            ascending=False
        )

        logger.info("")
        logger.info("Top 15 Important Features")

        logger.info(
            "\n%s",
            importance.head(15).to_string(index=False)
        )

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

        self.split_data()

        self.train()

        self.evaluate()

        self.feature_importance()

        self.save_model()


if __name__ == "__main__":

    trainer = ClassifierTrainer(
        data_path="data/processed/processed_dataset.csv",
        model_path="models/random_forest.pkl"
    )

    trainer.run()