from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd

from src.api.dependencies import (
    isolation_model,
    classifier_model
)

from src.ml.feature_engineering import FeatureEngineer
from src.ml.predict import ThreatPredictor

router = APIRouter()

engineer = FeatureEngineer(
    input_path="",
    output_path="",
    scaler_path="models/scaler.pkl"
)

predictor = ThreatPredictor(
    isolation_model,
    classifier_model
)


@router.post("/predict-file")
async def predict_file(file: UploadFile = File(...)):

    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported."
        )

    try:
        df = pd.read_csv(
            file.file,
            low_memory=False
        )
    except UnicodeDecodeError:
        file.file.seek(0)
        df = pd.read_csv(
            file.file,
            encoding="latin-1",
            low_memory=False
        )

    processed = engineer.transform_dataframe(df)

    predictions = predictor.predict_dataframe(processed)

    total = len(predictions)

    attacks = int((predictions["prediction"] == "Attack").sum())
    benign = int((predictions["prediction"] == "Benign").sum())
    anomalies = int(predictions["anomaly"].sum())

    attack_percentage = round((attacks / total) * 100, 2)
    benign_percentage = round((benign / total) * 100, 2)

    avg_confidence = round(
        float(predictions["confidence"].mean()),
        2
    )

    if attack_percentage >= 50:
        risk_level = "Critical"
        risk_color = "#DC2626"
    elif attack_percentage >= 20:
        risk_level = "High"
        risk_color = "#EA580C"
    elif attack_percentage >= 5:
        risk_level = "Medium"
        risk_color = "#EAB308"
    else:
        risk_level = "Low"
        risk_color = "#16A34A"

    

    attacks_df = predictions[
    predictions["prediction"] == "Attack"
].sort_values(
    by=["confidence", "anomaly_score"],
    ascending=[False, True]
).head(50)
    benign_df = predictions[predictions["prediction"] == "Benign"].head(50)

    attacks_df["Severity"] = attacks_df.apply(
        lambda row: "Critical" if row["anomaly"] else "High",
        axis=1
    )

    benign_df["Severity"] = "Safe"

    threats = pd.concat(
        [attacks_df, benign_df],
        ignore_index=True
    )

    return {
        "filename": file.filename,
        "summary": {
            "total_records": total,
            "benign": benign,
            "attacks": attacks,
            "anomalies": anomalies
        },
        "statistics": {
            "attack_percentage": attack_percentage,
            "benign_percentage": benign_percentage,
            "average_confidence": avg_confidence
        },
        "risk": {
            "level": risk_level,
            "color": risk_color
        },
        "threats": threats.to_dict("records"),
"top_attacks": attacks_df.sort_values(
    by="confidence",
    ascending=False
).head(10).to_dict("records")
    }