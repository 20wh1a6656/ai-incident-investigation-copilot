# Architecture Design - AI Incident Investigation Copilot

This document outlines the software architecture of the **AI Incident Investigation Copilot**, focusing on the modular agent-based execution flow, RAG pipeline integration, database storage structures, and React frontend elements.

## System Workflow Diagram

```mermaid
graph TD
    User([User Client]) -->|1. Submit Incident Details| IngestAPI[FastAPI: /api/incidents/ingest]
    IngestAPI -->|2. Persist Raw Outage| SQLite[(SQLite Database)]
    User -->|3. Run AI Diagnosis| DiagnoseAPI[FastAPI: /api/incidents/{id}/diagnose]
    DiagnoseAPI -->|4. Trigger Orchestrator| Orchestrator[Investigation Orchestrator]
    
    subgraph Agentic Pipeline Stages
        Orchestrator -->|Stage 1: Analyze| AnalysisAgent[Incident Analysis Agent]
        Orchestrator -->|Stage 2: Retrieve| RetrievalAgent[Knowledge Retrieval Agent]
        Orchestrator -->|Stage 3: Correlate| RootCause[Root Cause Analyzer]
        Orchestrator -->|Stage 4 & 5: Plan| PlannerAgent[Investigation Planner Agent]
    end

    RetrievalAgent -->|Semantic Match Query| RAG[RAG Retrieval module]
    RAG -->|Similarity Search| ChromaDB[(ChromaDB Vector Store)]
    
    PlannerAgent -->|Read Prompts| Prompts[prompts/*.txt Templates]
    
    Orchestrator -->|5. Save Results| SQLite
    Orchestrator -->|6. Return State Payload| User
```

## Backend Modules

### 1. Agents Layer (`app/agents/`)
Specialized agents execute sequential reasoning loops:
- **Incident Analysis Agent**: Interrogates description texts and log stack traces using standard regex classifiers (and future LLM adapters) to identify classification categories, confidence index parameters, and verify severity levels.
- **Knowledge Retrieval Agent**: Interfaces with the local RAG engine to find matching SOPs.
- **Investigation Planner Agent**: Uses prompt template directives to format runbooks, checklists, priorities, and escalation structures.

### 2. Orchestration (`app/orchestrators/`)
Coordinates agent executions and handles state transfers:
- **Investigation Orchestrator**: Maintains the `InvestigationState` pipeline. Tracks execution stages (Stage 1 to 5), aggregates console timeline audits, captures diagnostic errors, and commits final reports to SQLite.

### 3. RAG Pipeline (`app/rag/`)
Handles the lifecycle of vectorized engineering runbooks:
- **Chroma Manager**: Client initialization wrapper pointing to `data/chroma_db`.
- **Ingest**: Generates embeddings using the local `SentenceTransformer` model (`all-MiniLM-L6-v2`) and indexes them.
- **Retrieve**: Performs similarity scans against the vector collection, falling back to a keyword-matching index if Chroma is offline.

### 4. Database Layer (`app/db/`)
- **SQLAlchemy + SQLite**: Defines simple schemas for `Incident` entries, `IncidentResult` triage payloads, and `KnowledgeBaseDoc` runbook reference tables.
