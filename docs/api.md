# REST API Specifications - AI Incident Investigation Copilot

The backend service runs a FastAPI web server exposing the following endpoints:

---

## 1. Incidents Endpoints

### Ingest Outage
- **Endpoint**: `POST /api/incidents/ingest`
- **Payload**:
  ```json
  {
    "description": "Checkout service throwing Hikari connection dropouts",
    "alarms": "Datadog Pager #998",
    "logs": "org.postgresql.util.PSQLException: FATAL...",
    "env": "prod-us-east",
    "severity": "P1"
  }
  ```
- **Response** (201 Created):
  ```json
  {
    "id": "e0e2d19b-c40d-4530-8025-05513f5fe844",
    "description": "Checkout service throwing Hikari connection dropouts",
    "alarms": "Datadog Pager #998",
    "logs": "org.postgresql.util.PSQLException: FATAL...",
    "env": "prod-us-east",
    "severity": "P1",
    "classification": null,
    "confidence": null,
    "duration": null,
    "created_at": "2026-06-14T10:00:00Z"
  }
  ```

### Run Triage Diagnosis
- **Endpoint**: `POST /api/incidents/{incident_id}/diagnose`
- **Response** (200 OK):
  ```json
  {
    "success": true,
    "incident_id": "e0e2d19b-c40d-4530-8025-05513f5fe844",
    "duration": "1.02s",
    "classification": "Database Connection Pool Exhaustion",
    "confidence": 96,
    "results": {
      "root_causes": [{"title": "HikariCP Connection Pool Starvation", "percentage": 96}],
      "evidence": {
        "sopName": "SOP-094: PostgreSQL Scale Limits",
        "snippet": "...",
        "source": "Confluence Wiki Runbooks",
        "strength": "98% Match"
      },
      "runbook": [{"step": "...", "detail": "..."}],
      "actions": [{"title": "...", "priority": "..."}],
      "escalation": {"team": "...", "level": "...", "reason": "..."},
      "checklist": ["..."],
      "audit": ["Orchestrator: Pipeline initialized...", "..."]
    }
  }
  ```

### Retrieve History List
- **Endpoint**: `GET /api/incidents/history`
- **Response** (200 OK):
  ```json
  [
    {
      "id": "e0e2d19b-c40d-4530-8025-05513f5fe844",
      "description": "...",
      "severity": "P1",
      "classification": "Database Connection Pool Exhaustion",
      "created_at": "2026-06-14T10:00:00Z"
    }
  ]
  ```

---

## 2. Knowledge Base Endpoints

### Index Document
- **Endpoint**: `POST /api/incidents/kb`
- **Payload**:
  ```json
  {
    "title": "SOP-094: PostgreSQL Connection Scans",
    "content": "Check database pools...",
    "source": "Confluence Wiki Runbooks"
  }
  ```

### List Documents
- **Endpoint**: `GET /api/incidents/kb`

---

## 3. System Endpoints

### Check Health & Connectivity
- **Endpoint**: `GET /api/system/health`
- **Response**:
  ```json
  {
    "status": "healthy",
    "database": { "status": "connected" },
    "rag": {
      "library_loaded": true,
      "chroma_connected": true,
      "collection_loaded": true,
      "storage_path": "../data/chroma_db"
    }
  }
  ```
