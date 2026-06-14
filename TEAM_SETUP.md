# AI Incident Triage Copilot: Teammate Setup Guide

Welcome to the team! This document contains instructions for setting up the local development environment, running the multi-agent backend and the React frontend, and verifying everything is functional.

---

## 1. System Requirements

* **Python**: `3.10.x` or `3.11.x`
* **Node.js**: `v20.x` (LTS recommended)
* **OS**: Windows, macOS, or Linux

---

## 2. Backend Environment Setup

The backend FastAPI service handles RAG vector searches (ChromaDB), incident audits (SQLite), and agentic reasoning orchestrations.

1. **Navigate to the Backend Directory**:
   ```bash
   cd backend
   ```

2. **Create a Python Virtual Environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:
   * **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   * **macOS / Linux (Bash)**:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Local Configurations (`backend/.env`)**:
   Verify your local `.env` file matches the template below:
   ```env
   # API keys & Providers
   ACTIVE_PROVIDER=mock
   OPENAI_API_KEY=your-api-key-here
   
   # Server Port and Host
   PORT=8000
   HOST=0.0.0.0
   ```

---

## 3. Ingestion & Database Initialization

Before starting the server, seed the local relational DB and the ChromaDB vector database with SRE Standard Operating Procedures (SOPs).

1. **Ingest SOPs**:
   From the active virtual environment in the `backend` folder, run:
   ```bash
   python run_sop_ingestion.py
   ```
   *This reads the standard runbooks under `data/sops/` and embeds 261 text chunks into the local Chroma vector store.*

2. **Verify Databases**:
   Ensure `data/incidents.db` and the folder `data/chroma_db/` are populated.

---

## 4. Run the Backend FastAPI Server

Start the backend locally on port 8000:
```bash
python run.py
```
* **API Documentation**: Access Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs)
* **Health Check**: Verify [http://localhost:8000/api/health](http://localhost:8000/api/health) returns `{"status":"healthy"}`.

---

## 5. Frontend Environment Setup

The React frontend utilizes Vite for build orchestration and Tailwind CSS for styling.

1. **Navigate to the Frontend Directory**:
   ```bash
   cd ../frontend
   ```

2. **Install Node Modules**:
   ```bash
   npm install
   ```

3. **Start the Frontend Dev Server**:
   ```bash
   npm run dev
   ```
   *By default, the Vite dev server boots on [http://localhost:3000](http://localhost:3000) and proxies `/api` calls directly to `http://localhost:8000`.*

---

## 6. Running Tests

To verify backend agent reasoning, classifications, and thresholds locally:

1. Make sure you are in the `backend` directory with your `venv` activated.
2. Execute the automated test suite using pytest:
   ```bash
   pytest test_pipeline.py
   ```

All test cases should pass against the local SQLite database and Chroma vector engine.

---

## 7. Archived Files

* **`archive/tests/`**: Contains legacy one-off developer scratch testing files used during initial prototyping (e.g. `test_case.py`, `run_rag_test.py`, `run_investigator_test.py`).
* **`archive/databases/`**: Contains pre-compiled SQLite databases generated during initial debugging sessions. Kept strictly for reference in case troubleshooting is needed.
