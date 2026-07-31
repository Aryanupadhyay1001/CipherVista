# CipherVista - API Design

**Version:** 1.0  
**Project Type:** AI-Powered Threat Intelligence Platform  
**Status:** Planning Phase

---

# 1. Introduction

This document defines the REST API endpoints exposed by the CipherVista backend.

The backend is implemented using FastAPI and acts as the communication layer between the dashboard, machine learning engine, AI engine, and database.

All responses are returned in JSON format.

---

# 2. API Overview

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /upload | Upload a network traffic dataset |
| POST | /predict | Detect anomalous records |
| POST | /generate-report | Generate AI incident report |
| GET | /incidents | Retrieve all incidents |
| GET | /incident/{id} | Retrieve a specific incident |
| DELETE | /incident/{id} | Delete an incident |

---

# 3. Upload Dataset

### Endpoint

POST /upload

### Purpose

Uploads a CSV dataset for analysis.

### Request

Content-Type: multipart/form-data

Parameter

| Name | Type | Required |
|------|------|----------|
| file | CSV File | Yes |

### Success Response

```json
{
    "message": "Dataset uploaded successfully",
    "filename": "Friday.csv"
}
```

---

# 4. Predict Threats

### Endpoint

POST /predict

### Purpose

Runs the Machine Learning model on the uploaded dataset.

### Request

```json
{
    "filename":"Friday.csv"
}
```

### Success Response

```json
{
    "total_records":22500,
    "anomalies":38,
    "status":"Prediction Completed"
}
```

---

# 5. Generate AI Report

### Endpoint

POST /generate-report

### Purpose

Generates an AI-powered report for detected anomalies.

### Request

```json
{
    "incident_id":12
}
```

### Success Response

```json
{
    "severity":"High",
    "summary":"Unusual outbound traffic detected.",
    "recommendation":"Investigate endpoint immediately."
}
```

---

# 6. Get Incident History

### Endpoint

GET /incidents

### Purpose

Returns all stored incidents.

### Success Response

```json
[
    {
        "incident_id":1,
        "severity":"Medium",
        "status":"Open"
    },
    {
        "incident_id":2,
        "severity":"High",
        "status":"Resolved"
    }
]
```

---

# 7. Get Incident Details

### Endpoint

GET /incident/{id}

### Purpose

Returns complete information about a specific incident.

### Success Response

```json
{
    "incident_id":15,
    "prediction":"Anomaly",
    "severity":"High",
    "threat_score":92,
    "summary":"Potential brute force attack.",
    "recommendation":"Block source IP and investigate logs."
}
```

---

# 8. Delete Incident

### Endpoint

DELETE /incident/{id}

### Purpose

Deletes an incident from the database.

### Success Response

```json
{
    "message":"Incident deleted successfully."
}
```

---

# 9. HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Resource Created |
| 400 | Invalid Request |
| 404 | Resource Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

---

# 10. API Workflow

```
Dashboard

↓

FastAPI

↓

Validate Request

↓

ML Engine

↓

Database

↓

AI Engine

↓

Return JSON Response

↓

Dashboard
```

---

# 11. Design Principles

- RESTful API Design
- JSON-based communication
- Stateless requests
- Modular endpoint structure
- Clear error responses
- Easy integration with future frontend applications

---

# 12. Future API Endpoints

The following endpoints are planned for future versions:

- POST /live-monitor
- POST /mitre-map
- POST /ioc-extract
- POST /cve-lookup
- GET /dashboard/analytics
- POST /chat

These endpoints will support advanced threat intelligence and AI-powered security analysis.