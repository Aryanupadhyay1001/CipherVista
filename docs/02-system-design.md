# CipherVista - System Design

**Version:** 1.0

---

# 1. Purpose

This document describes the overall system design of CipherVista Version 1, including its architecture, modules, request flow, responsibilities, and interactions.

The objective is to design a modular, scalable, and maintainable AI-powered threat intelligence platform.

---

# 2. System Overview

CipherVista consists of six major components:

1. Dashboard
2. Backend API
3. Machine Learning Engine
4. AI Engine
5. Database
6. Dataset Processing Pipeline

Each component has a single responsibility and communicates through the backend.

---

# 3. High-Level Architecture

```
                    +-----------------------+
                    |  Streamlit Dashboard  |
                    +-----------+-----------+
                                |
                                |
                                ▼
                    +-----------------------+
                    |    FastAPI Backend    |
                    +----+-----------+------+
                         |           |
                         |           |
               +---------+           +-----------+
               |                                 |
               ▼                                 ▼
      +----------------+               +----------------+
      |   ML Engine    |               |   AI Engine    |
      | IsolationForest|               | Gemini API     |
      +-------+--------+               +--------+-------+
              |                                  |
              +---------------+------------------+
                              |
                              ▼
                     +--------------------+
                     |  SQLite Database   |
                     +--------------------+
```

---

# 4. Request Flow

A typical user interaction follows the sequence below.

```
User
 │
 ▼
Upload CSV
 │
 ▼
Validate Dataset
 │
 ▼
Preprocess Dataset
 │
 ▼
Feature Engineering
 │
 ▼
Load ML Model
 │
 ▼
Predict Anomalies
 │
 ▼
Calculate Threat Score
 │
 ▼
Store Incident
 │
 ▼
Generate AI Report
 │
 ▼
Store AI Report
 │
 ▼
Display Dashboard
```

---

# 5. Module Responsibilities

## Dashboard

Responsibilities

- Upload CSV datasets
- Display prediction results
- Show threat analytics
- Display AI-generated reports
- View incident history

---

## Backend API

Responsibilities

- Accept client requests
- Validate input
- Coordinate modules
- Return responses
- Handle errors

---

## Machine Learning Engine

Responsibilities

- Data preprocessing
- Feature engineering
- Model loading
- Prediction
- Threat scoring

---

## AI Engine

Responsibilities

- Prompt generation
- Gemini API communication
- Incident explanation
- Recommendation generation

---

## Database

Responsibilities

- Store uploaded datasets
- Store incidents
- Store AI reports
- Maintain history

---

# 6. Core Workflow

The backend acts as the central coordinator.

It never performs machine learning directly.

Instead, it communicates with dedicated modules.

```
Dashboard
      │
      ▼
Backend API
      │
      ├────────► ML Engine
      │
      ├────────► AI Engine
      │
      └────────► Database
```

---

# 7. Data Flow

Input

CSV Dataset

↓

Preprocessing

↓

Feature Engineering

↓

Machine Learning Prediction

↓

Threat Score

↓

Incident Object

↓

AI Report

↓

Database

↓

Dashboard

---

# 8. Design Principles

CipherVista follows the principles below.

- Single Responsibility Principle
- Modular Design
- Separation of Concerns
- Reusable Components
- Scalability
- Maintainability

---

# 9. Version 1 Constraints

Version 1 processes uploaded datasets only.

The following capabilities are intentionally excluded.

- Live packet capture
- Real-time streaming
- Distributed processing
- Multi-agent architecture
- Cloud deployment

These features are planned for future versions.

---

# 10. Summary

CipherVista Version 1 is designed as a layered architecture where the backend coordinates machine learning, artificial intelligence, and persistent storage while presenting results through an interactive dashboard.

This modular design allows future versions to introduce additional capabilities without major architectural changes.