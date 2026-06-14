import os
import sys

# Ensure backend root is on sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.db import crud, models
from app.orchestrators.investigation import investigation_orchestrator
from app.rag.chroma_manager import chroma_manager
from sentence_transformers import SentenceTransformer

def main():
    print("====================================================")
    print("     Multi-Symptom Incident Pipeline Audit         ")
    print("====================================================\n")

    # 1. Setup in-memory / temporary database to isolate test
    test_db_path = "audit_incidents.db"
    if os.path.exists(test_db_path):
        try:
            os.remove(test_db_path)
        except Exception:
            pass

    test_db_url = f"sqlite:///{test_db_path}"
    engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # 2. Ingest the multi-symptom incident
    desc = """Users cannot login to VPN.
SSO portal unavailable.
Email notifications failing.
Multiple services reporting authentication errors.
LDAP bind failures observed."""

    incident = crud.create_incident(
        db=db,
        description=desc,
        alarms="MFA gateway callback failures, LDAP lookup timeouts",
        logs="ldap_bind: authentication failure, error code 49; smtp_auth: credentials invalid",
        env="production-shared-infra",
        severity="P1"
    )

    print(f"Incident seeded in database with ID: {incident.id}\n")

    # 3. Run RAG query for top 10 chunks manually to display them
    client = chroma_manager.client
    collection = client.get_collection("incident_runbooks")
    encoder = SentenceTransformer("all-MiniLM-L6-v2")
    
    print("--- 1. TOP 10 RETRIEVED SOP CHUNKS & SIMILARITY SCORES ---")
    query_embedding = encoder.encode(desc).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=10
    )
    
    retrieved_chunks = []
    if results and results.get("documents") and len(results["documents"]) > 0:
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        ids = results["ids"][0]
        
        for rank, (doc_id, doc, meta, dist) in enumerate(zip(ids, documents, metadatas, distances)):
            similarity_pct = round((1.0 - (dist / 2.0)) * 100, 1) if dist else 85.0
            print(f"Rank {rank+1}: [{doc_id}] {meta['title']} | Section: {meta['section']} (Score: {similarity_pct}%)")
            retrieved_chunks.append({
                "id": doc_id,
                "title": meta['title'],
                "section": meta['section'],
                "score": similarity_pct
            })
    else:
        print("No matches found in ChromaDB.")
    print("")

    # 4. Run the full Orchestrator Pipeline
    print("--- 2. PIPELINE EXECUTION TRACE ---")
    state = investigation_orchestrator.run_diagnosis(db, incident.id)
    for log_line in state.console_audit:
        print(f"  {log_line}")
    print("")

    # 5. Extract results from state
    print("--- 3. CANDIDATE CLASSIFICATIONS ---")
    candidates = state.evidence.get("candidates", [])
    for idx, cand in enumerate(candidates):
        print(f"  {idx+1}. {cand['name']} (Score: {cand['score']})")
    print("")

    print("--- 4. CLASSIFICATION REASONING ---")
    print(f"  {state.evidence.get('classification_reasoning')}")
    print(f"  Selected: '{state.classification}' with {state.confidence}% confidence.")
    print("")

    print("--- 5. SELECTED ROOT CAUSES ---")
    for rc in state.root_causes:
        print(f"  - {rc['title']} (Strength: {rc['strength']}, Probability: {rc['percentage']}%)")
    print("")

    print("--- 6. SELECTED ACTION PLAN ---")
    print("  Recommended Actions:")
    for act in state.actions:
        print(f"    - {act['title']} (Priority: {act['priority']})")
    print("  Runbook Steps:")
    for idx, step in enumerate(state.runbook):
        print(f"    {idx+1}. {step['step']}: {step['detail']}")
    print("  Escalation Matrix:")
    esc = state.escalation
    print(f"    - Team: {esc['team']} (Level: {esc['level']})")
    print(f"      Reason: {esc['reason']}")
    print(f"      Pod: {esc['group']}")
    print("  Verification Checklist:")
    for item in state.checklist:
        print(f"    - [ ] {item}")
    print("")

    # Clean up test SQLite database file
    db.close()
    try:
        os.remove(test_db_path)
    except Exception:
        pass

if __name__ == "__main__":
    main()
