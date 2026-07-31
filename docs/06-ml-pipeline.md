# CipherVista - Machine Learning Pipeline

**Version:** 1.0  
**Project Type:** AI-Powered Threat Intelligence Platform  
**Model:** Isolation Forest

---

# 1. Introduction

This document describes the Machine Learning pipeline used in CipherVista Version 1.

The pipeline is responsible for transforming raw network traffic data into anomaly predictions that can be analyzed by the AI Engine.

The objective is to accurately identify suspicious network activities while maintaining a modular and reusable workflow.

---

# 2. Pipeline Overview

The Machine Learning pipeline consists of the following stages.

```
CSV Dataset

↓

Data Validation

↓

Data Cleaning

↓

Feature Engineering

↓

Feature Scaling

↓

Model Training

↓

Model Saving

↓

Model Loading

↓

Prediction

↓

Threat Score Generation
```

---

# 3. Pipeline Stages

## Stage 1 – Dataset Ingestion

Responsibilities

- Read CSV dataset
- Verify file format
- Load into a Pandas DataFrame

Input

- CSV File

Output

- DataFrame

---

## Stage 2 – Data Cleaning

Responsibilities

- Remove duplicate records
- Handle missing values
- Remove unnecessary columns
- Correct invalid values

Output

- Clean DataFrame

---

## Stage 3 – Feature Engineering

Responsibilities

- Select relevant features
- Encode categorical variables
- Convert data types
- Prepare model input

Output

- Feature Matrix

---

## Stage 4 – Feature Scaling

Responsibilities

- Normalize numerical features
- Improve model performance
- Prepare consistent input

Output

- Scaled Feature Matrix

---

## Stage 5 – Model Training

Algorithm

Isolation Forest

Responsibilities

- Train anomaly detection model
- Learn normal network behavior
- Identify anomalous observations

Output

- Trained Model

---

## Stage 6 – Model Persistence

Responsibilities

- Save trained model using Joblib
- Load model during prediction

Output

- model.pkl

---

## Stage 7 – Prediction

Responsibilities

- Load saved model
- Predict anomalies
- Assign anomaly labels

Output

Normal Traffic

or

Anomalous Traffic

---

## Stage 8 – Threat Score Generation

Responsibilities

Convert anomaly scores into a user-friendly threat score.

Example

| Anomaly Score | Threat Score | Severity |
|---------------|--------------|----------|
| 0.10 | 15 | Low |
| 0.35 | 45 | Medium |
| 0.62 | 72 | High |
| 0.91 | 95 | Critical |

---

# 4. Complete Pipeline

```
Raw Dataset

↓

Validation

↓

Cleaning

↓

Feature Engineering

↓

Scaling

↓

Isolation Forest

↓

Prediction

↓

Threat Score

↓

Incident Object

↓

AI Report
```

---

# 5. Model Selection

The primary algorithm used in Version 1 is Isolation Forest.

Reasons for selecting Isolation Forest:

- Designed for anomaly detection
- Works without labeled data
- Efficient on large datasets
- Robust for cybersecurity use cases
- Easy to explain during interviews

---

# 6. Project Files

The Machine Learning module consists of the following files.

```
src/ml/

preprocess.py

feature_engineering.py

train.py

predict.py
```

---

# 7. Responsibilities of Each File

## preprocess.py

- Read dataset
- Clean data
- Handle missing values
- Remove duplicates

---

## feature_engineering.py

- Select features
- Encode categorical values
- Scale numerical features

---

## train.py

- Train Isolation Forest
- Evaluate model
- Save trained model

---

## predict.py

- Load saved model
- Predict anomalies
- Generate threat scores

---

# 8. Output of ML Engine

The Machine Learning Engine produces an Incident object.

Example

```json
{
    "prediction": "Anomaly",
    "anomaly_score": 0.87,
    "threat_score": 91,
    "severity": "Critical"
}
```

This object is passed to the AI Engine for report generation.

---

# 9. Future Improvements

Future versions may introduce:

- XGBoost
- Autoencoders
- Deep Learning Models
- Ensemble Models
- Online Learning
- Model Comparison Dashboard

---

# 10. Summary

The Machine Learning pipeline of CipherVista follows a structured workflow beginning with data ingestion and ending with threat scoring. The modular design allows individual stages to be improved or replaced without affecting the rest of the system, ensuring maintainability and scalability.