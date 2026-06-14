# Retrieval Audit Report - ChromaDB RAG Pipeline

This document presents the diagnostic audit of the RAG (Retrieval-Augmented Generation) indexing system for the **AI Incident Investigation Copilot**.

---

## 1. Inventory Summary

- **Number of SOP Files**: **5 files** found in the `data/` directory:
  1. `data/app_crash.md`
  2. `data/db_connectivity.md`
  3. `data/email_failure.md`
  4. `data/sso_failure.md`
  5. `data/vpn_failure.md`
- **Number of Vector Records (ChromaDB)**: **0 records**.
  - **Reason**: The SQLite schema seeder in `backend/app/main.py` inserts references into the SQL database during startup but does not call the vector ingestion routines. ChromaDB collections remain unpopulated unless `backend/app/rag/ingest.py` is invoked manually.
  - **Result**: The retriever always switches to its built-in `_keyword_lookup_fallback` logic.

---

## 2. Test Query Retrieval Results

Below are the computed results of the RAG keyword matching query scoring:

### Test Query A: `"Users cannot login to VPN"`
- **Top 3 Matches**:
  1. **VPN Gateway Connection Failure** (`vpn_failure`): **80.0% Match** (Keyword matched: `"vpn"`)
  2. **General Triaging Guide** (`generic_sop`): **50.0% Match** (Default fallback)
- **Evaluation**: Correct. It retrieves the VPN-specific SOP because no other documents match.

### Test Query B: `"SMTP authentication failing"`
- **Top 3 Matches**:
  1. **SSO Authentication Failures** (`sso_failure`): **80.0% Match** (Keyword matched: `"authentication"`)
  2. **SMTP / Email Notification Delivery Failures** (`email_failure`): **80.0% Match** (Keyword matched: `"smtp"`)
  3. **General Triaging Guide** (`generic_sop`): **50.0% Match**
- **Evaluation**: **FAIL (Bug Discovery)**. The query resolves `SOP-102: Single Sign-On (SSO)` as the top result. Because both SSO and Email SOPs matched exactly 1 keyword, their score tied at 80%. Due to python's stable sorting, the list returns whichever was defined first in the fallback array. Since `sso_failure` precedes `email_failure`, Okta SSO is returned instead of the SMTP document.

### Test Query C: `"Database connection pool exhausted"`
- **Top 3 Matches**:
  1. **PostgreSQL Connection Pool Exhaustion** (`db_connectivity`): **90.0% Match** (Keywords matched: `"database"`, `"connection"`, `"pool"`)
  2. **General Triaging Guide** (`generic_sop`): **50.0% Match**
- **Evaluation**: Correct. The PostgreSQL connection document matches multiple target terms, yielding a high score.

---

## 3. Discovered Bugs & Root Causes

1. **Unindexed ChromaDB Collection**: Seeding script only populates SQL, leaving the vector store empty.
2. **Stable Sorting Collision (Tie-breaker Bug)**: In `retrieve.py`, queries containing generic terms like `"authentication"` cause collisions between unrelated SOPs (SSO vs Email) that carry the same score.
3. **Retrieve Limit Constraint**: In `knowledge_retrieval.py` line 23, the orchestrator invokes retrieval with `limit=1`, meaning only the top-1 document is passed down, causing planner diagnostics to be thin and restrict the visible choices.
