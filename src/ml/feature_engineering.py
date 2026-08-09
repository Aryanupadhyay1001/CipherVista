import os
import logging
import joblib
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler, LabelEncoder
from src.ml.feature_schema import FEATURE_COLUMNS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class FeatureEngineer:

    def __init__(self, input_path, output_path, scaler_path):
        self.input_path = input_path
        self.output_path = output_path
        self.scaler_path = scaler_path
        self.data = None

    def load_data(self):

        logger.info("Loading processed dataset in chunks...")

        chunks = []

        chunk_size = 100000
        sample_fraction = 0.18

        for i, chunk in enumerate(
            pd.read_csv(
                self.input_path,
                chunksize=chunk_size,
                low_memory=False
            )
        ):

            chunk.columns = chunk.columns.str.strip()

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

    def remove_unused_columns(self):

        logger.info("Removing non-feature columns...")

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

    def encode_label(self):

        logger.info("Encoding attack labels...")

        encoder = LabelEncoder()

        self.data["Label"] = encoder.fit_transform(
            self.data["Label"]
        )

        os.makedirs(
            os.path.dirname("models/label_encoder.pkl"),
            exist_ok=True
        )

        joblib.dump(
            encoder,
            "models/label_encoder.pkl"
        )

        logger.info(
            f"{len(encoder.classes_)} classes encoded."
        )

        logger.info(
            f"Classes: {list(encoder.classes_)}"
        )

    def scale_features(self):

        logger.info("Scaling numerical features...")

        X = self.data[FEATURE_COLUMNS]
        y = self.data["Label"]

        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.apply(pd.to_numeric, errors="coerce")

        numeric_cols = X.select_dtypes(include=["number"]).columns

        X[numeric_cols] = X[numeric_cols].fillna(
            X[numeric_cols].median()
        )

        scaler = StandardScaler()

        X_scaled = scaler.fit_transform(X)

        os.makedirs(
            os.path.dirname(self.scaler_path),
            exist_ok=True
        )

        joblib.dump(
            scaler,
            self.scaler_path
        )

        logger.info("Scaler saved successfully.")

        X_scaled = pd.DataFrame(
            X_scaled,
            columns=X.columns
        )

        X_scaled["Label"] = y.values

        self.data = X_scaled

    def save_data(self):

        os.makedirs(
            os.path.dirname(self.output_path),
            exist_ok=True
        )

        self.data.to_csv(
            self.output_path,
            index=False
        )

        logger.info(
            "Feature engineered dataset saved."
        )

    def summary(self):

        logger.info("========== Feature Engineering ==========")
        logger.info(f"Rows : {self.data.shape[0]}")
        logger.info(f"Columns : {self.data.shape[1]}")
        logger.info("=========================================")

    def transform_dataframe(self, df):

        df = df.copy()

        df.columns = df.columns.str.strip()

        columns_to_drop = [
            "Flow ID",
            "Source IP",
            "Destination IP",
            "Timestamp"
        ]

        df.drop(
            columns=[c for c in columns_to_drop if c in df.columns],
            inplace=True
        )

        if "Label" in df.columns:

            y = df["Label"]

        else:

            y = None

        missing = [
            column
            for column in FEATURE_COLUMNS
            if column not in df.columns
        ]

        if missing:

            raise ValueError(
                f"Missing required features: {missing}"
            )

        X = df[FEATURE_COLUMNS]

        y = None

        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.apply(pd.to_numeric, errors="coerce")

        numeric_cols = X.select_dtypes(include=["number"]).columns

        X[numeric_cols] = X[numeric_cols].fillna(
            X[numeric_cols].median()
        )

        logger.info(
            f"Scaling {len(X.columns)} features."
        )

        scaler = joblib.load(
            self.scaler_path
        )

        X_scaled = scaler.transform(X)

        X_scaled = pd.DataFrame(
            X_scaled,
            columns=X.columns
        )

        if y is not None:
            X_scaled["Label"] = y.values

        return X_scaled

    def run(self):

        self.load_data()

        self.remove_unused_columns()

        self.encode_label()

        self.scale_features()

        self.save_data()

        self.summary()


if __name__ == "__main__":

    engineer = FeatureEngineer(
        input_path="data/processed/processed_dataset.csv",
        output_path="data/processed/final_dataset.csv",
        scaler_path="models/scaler.pkl"
    )

    engineer.run()