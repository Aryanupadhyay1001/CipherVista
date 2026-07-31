import os
import logging
import numpy as np
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class DataPreprocessor:
    def __init__(self, input_dir: str, output_path: str):
        self.input_dir = input_dir
        self.output_path = output_path
        self.data = None

    def load_data(self):
        csv_files = [
            file for file in os.listdir(self.input_dir)
            if file.endswith(".csv")
        ]

        if not csv_files:
            raise FileNotFoundError("No CSV files found.")

        datasets = []

        for file in csv_files:
            path = os.path.join(self.input_dir, file)

            logger.info(f"Loading {file}")

            try:
                df = pd.read_csv(path, low_memory=False)
            except UnicodeDecodeError:
                logger.warning(f"{file} is not UTF-8. Trying latin-1...")
                try:
                    df = pd.read_csv(path, encoding="latin-1", low_memory=False)
                except UnicodeDecodeError:
                    logger.warning(f"{file} is not latin-1. Trying cp1252...")
                    df = pd.read_csv(path, encoding="cp1252", low_memory=False)

            df.columns = df.columns.str.strip()

            datasets.append(df)

        self.data = pd.concat(
            datasets,
            ignore_index=True
        )

        logger.info(
            f"Merged {len(csv_files)} datasets "
            f"({self.data.shape[0]} rows, {self.data.shape[1]} columns)."
        )

    def clean_data(self):
        logger.info("Cleaning dataset...")

        self.data.columns = self.data.columns.str.strip()

        self.data.replace([np.inf, -np.inf], np.nan, inplace=True)

        duplicate_rows = self.data.duplicated().sum()
        if duplicate_rows > 0:
            logger.info(f"Removing {duplicate_rows} duplicate rows.")
            self.data.drop_duplicates(inplace=True)

        missing_before = self.data.isnull().sum().sum()

        numeric_columns = self.data.select_dtypes(include=np.number).columns
        self.data[numeric_columns] = self.data[numeric_columns].fillna(
            self.data[numeric_columns].median()
        )

        self.data.dropna(inplace=True)

        logger.info("Preserving original attack labels...")

        self.data["Label"] = self.data["Label"].astype(str).str.strip()

        self.data["Label"] = self.data["Label"].replace({
            "BENIGN": "Benign"
        })

        missing_after = self.data.isnull().sum().sum()

        logger.info(f"Missing values before cleaning: {missing_before}")
        logger.info(f"Missing values after cleaning: {missing_after}")

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
            f"Processed dataset saved to:\n{self.output_path}"
        )
    def summary(self):
        logger.info("========== Dataset Summary ==========")
        logger.info(f"Rows    : {self.data.shape[0]}")
        logger.info(f"Columns : {self.data.shape[1]}")
        logger.info("=====================================")

    def run(self):
        self.load_data()
        self.clean_data()
        self.save_data()
        self.summary()


if __name__ == "__main__":
    INPUT_DIR = "data/raw"
    OUTPUT_PATH = "data/processed/processed_dataset.csv"

    preprocessor = DataPreprocessor(
        INPUT_DIR,
        OUTPUT_PATH
    )

    preprocessor.run()