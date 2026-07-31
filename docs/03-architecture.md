# CipherVista - Architecture

**Version:** 1.0  
**Project Type:** AI-Powered Threat Intelligence Platform  
**Status:** Planning Phase

---

# 1. Introduction

This document describes the software architecture of CipherVista Version 1.

The application follows a modular layered architecture where each component has a well-defined responsibility. This design improves maintainability, readability, and scalability while keeping the codebase simple.

---

# 2. Architectural Style

CipherVista follows a **Layered Modular Architecture**.

```
                    Presentation Layer
                  (Streamlit Dashboard)
                            │
                            ▼
                   Application Layer
                    (FastAPI Backend)
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
  Machine Learning      AI Engine         Database Layer
      Engine           (Gemini API)         (SQLite)
        │                   │
        └───────────────┬───┘
                        ▼
                 Prediction Results
```

---

# 3. Folder Architecture

```
CipherVista/
│
├── dashboard/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│
├── models/
│
├── screenshots/
│
├── src/
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   │
│   ├── database/
│   │   ├── db.py
│   │   └── models.py
│   │
│   ├── llm/
│   │   ├── gemini.py
│   │   └── prompts.py
│   │
│   ├── ml/
│   │   ├── preprocess.py
│   │   ├── feature_engineering.py
│   │   ├── train.py
│   │   └── predict.py
│   │
│   ├── utils/
│   │   ├── config.py
│   │   └── logger.py
│   │
│   └── main.py
│
├── .env
├── README.md
├── requirements.txt
└── .gitignore
```

---

# 4. Layer Responsibilities

## Presentation Layer

Components

- Streamlit Dashboard

Responsibilities

- Accept user input
- Upload datasets
- Display prediction results
- Show AI reports
- Visualize analytics

---

## Application Layer

Components

- FastAPI Backend

Responsibilities

- Receive HTTP requests
- Validate requests
- Coordinate all modules
- Return API responses

---

## Machine Learning Layer

Components

- Preprocessing
- Feature Engineering
- Model Training
- Prediction

Responsibilities

- Clean data
- Prepare features
- Detect anomalies
- Calculate threat score

---

## AI Layer

Components

- Gemini Integration
- Prompt Templates

Responsibilities

- Generate incident summaries
- Explain anomalies
- Recommend mitigation steps

---

## Database Layer

Components

- SQLite
- SQLAlchemy Models

Responsibilities

- Store incidents
- Store AI reports
- Maintain upload history

---

# 5. Module Interaction

```
Dashboard
    │
    ▼
FastAPI
    │
    ├────────────► ML Engine
    │                 │
    │                 ▼
    │          Prediction Result
    │
    ├────────────► AI Engine
    │                 │
    │                 ▼
    │          Incident Report
    │
    └────────────► Database
                      │
                      ▼
                Stored Results
```

---

# 6. Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| Dashboard | User Interface |
| FastAPI | Application Logic |
| ML Engine | Threat Detection |
| AI Engine | Incident Analysis |
| Database | Data Persistence |
| Utils | Shared Configuration & Logging |

---

# 7. Architectural Decisions

### Layered Architecture

The project separates the user interface, business logic, machine learning, AI, and database into independent layers.

---

### Modular Design

Each module performs one primary responsibility and can evolve independently.

---

### Backend as Orchestrator

The FastAPI backend coordinates communication between all modules instead of embedding business logic in the dashboard.

---

### Machine Learning Before AI

The ML Engine first identifies anomalous records.

Only detected incidents are forwarded to the AI Engine for explanation, reducing unnecessary API usage and improving efficiency.

---

### Persistent Storage

All incidents and generated reports are stored in SQLite so users can review previous investigations.

---

# 8. Scalability

The architecture allows future integration of:

- Live packet capture
- Threat intelligence feeds
- MITRE ATT&CK mapping
- CVE enrichment
- Authentication
- Cloud deployment
- Multi-agent AI

These additions can be implemented without changing the overall architecture.

---

# 9. Benefits

- Clean separation of concerns
- Easy to maintain
- Easy to test
- Scalable architecture
- Professional project structure
- Suitable for production-grade expansion

---

# 10. Summary

CipherVista uses a modular layered architecture in which the FastAPI backend acts as the central coordinator between the Dashboard, Machine Learning Engine, AI Engine, and Database. This approach ensures maintainability, extensibility, and a clear separation of responsibilities while providing a strong foundation for future versions of the platform.