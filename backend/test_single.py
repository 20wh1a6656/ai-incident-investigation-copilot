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

def main():
    db_path = "debug_pipeline.db"
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception:
            pass

    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    desc = """Users cannot login to VPN.
SSO portal unavailable.
Email notifications failing.
Multiple services reporting authentication errors.
LDAP bind failures observed."""
    incident = crud.create_incident(
        db=db,
        description=desc,
        alarms="SSO portal HTTP 503, LDAP timeouts",
        logs="ldap_bind error: code 49; smtp credentials mismatch",
        env="prod-infra",
        severity="P1"
    )
    
    state = investigation_orchestrator.run_diagnosis(db, incident.id)
    
    print("\n=== DEBUG OUTPUT ===")
    print(f"Classification: {state.classification}")
    print(f"Confidence: {state.confidence}")
    print(f"Candidates:")
    for c in state.evidence.get("candidates", []):
        print(f"  - {c['name']}: Score {c['score']} ({c['percentage']}%)")
        
    print("\nRetrieval details:")
    retrieved = state.evidence.get("retrieved_chunks", [])
    for idx, chunk in enumerate(retrieved):
        print(f"  {idx+1}. {chunk.get('id')} - {chunk.get('title')} - Score: {chunk.get('confidence_score')}%")

    print("\nEvidence summary categories:")
    summary = state.evidence.get("evidence_summary", {})
    categories = summary.get("categories", {})
    for cat, info in categories.items():
        print(f"  {cat}:")
        print(f"    retrieved_chunks_count: {info.get('retrieved_chunks_count')}")
        print(f"    supporting_signals: {info.get('supporting_signals')}")
        print(f"    conflicting_signals: {info.get('conflicting_signals')}")

    db.close()
    try:
        os.remove(db_path)
    except Exception:
        pass

if __name__ == "__main__":
    main()
