# AI Incident Investigation Copilot

An enterprise-ready incident triage dashboard that takes ambiguous downstream symptoms, logs, and monitoring telemetry and uses specialized agents to generate incident classifications, root causes, RAG evidence search results, recommended recovery runbooks, prioritized actions, escalation plans, and checklists.

---

## Architecture Overview

This project is built around the **Agentic Orchestration Pattern**:
1. **FastAPI Backend**: Serves API endpoints, hosts SQLite models via SQLAlchemy, and houses RAG search and agent engines.
2. **Specialized Agents**: Decoupled modules (`incident_analysis`, `knowledge_retrieval`, and `investigation_planner`) manage logical steps of triaging.
3. **Orchestrator**: The central `InvestigationOrchestrator` runs state machine transitions, passing `InvestigationState` objects, generating timeline audit trails, and persisting records.
4. **Vector RAG Layer**: Employs `sentence-transformers` and `ChromaDB` to perform similarity checks against stored SOPs (with robust keyword fallbacks).
5. **Tailwind v4 React Frontend**: Built on Vite, React Router, and Axios, displaying premium dark-themed glassmorphic components, skeleton shimmers, and dynamic modal controls.

---

## Folder Structure

```
ai-incident-investigation-copilot/
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── agents/           # Specialized Agent Classes
│   │   ├── db/               # SQLite Models & Sessions
│   │   ├── orchestrators/     # Workflows coordinator
│   │   ├── prompts/          # Externalized Prompt Templates
│   │   ├── rag/              # ChromaDB & Vector embedding scripts
│   │   ├── routers/          # API Route handlers
│   │   └── schemas/          # Data Validation schemas
│   └── run.py                # Server runner helper
├── frontend/                 # React+Vite Frontend
│   ├── src/
│   │   ├── components/       # Custom Glassmorphism UI modules
│   │   ├── pages/            # Dashboard & KB pages
│   │   └── services/         # Axios API client
│   └── index.html            # Dark shell container
├── docs/                     # Architecture & API reference documents
└── data/                     # Local SQLite and Chroma file databases
```

---

## Setup & Running Guide

### Prerequisite: Node.js & Python
A portable Node version is configured inside the scratch folder:
`C:/Users/Hp/.gemini/antigravity/scratch/node-portable/node-v20.13.1-win-x64`

### 1. Running the Backend API
Navigate to the `backend/` folder, configure a Python virtual environment, install the requirements list, and run:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```
The FastAPI documentation will be available at: http://localhost:8000/docs

### 2. Running the Frontend React App
Navigate to the `frontend/` folder, run npm install, and start the development server:

```bash
cd frontend
# Using the local portable node
$env:Path = "C:\Users\Hp\.gemini\antigravity\scratch\node-portable\node-v20.13.1-win-x64;" + $env:Path
npm install
npm run dev
```
The React hot-reload dev client will be running at: http://localhost:3000

---

## Environment Variables Configuration

Create a `.env` file inside `backend/` (or copy `.env.example`):
- `ACTIVE_PROVIDER`: Set to `mock` for local standalone analysis. Future integrations can set it to `openai` or `github`.
- `SQLITE_DB_PATH`: Location of the SQLite database.
- `CHROMA_DB_PATH`: Location of ChromaDB vector indexes.
