import os
import sys
import shutil

# Ensure backend root is on sys.path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.db import crud, models
from app.orchestrators.investigation import investigation_orchestrator
from app.rag.ingest import doc_ingestor

def run_integration_test():
    print("====================================================")
    print("     E2E Integration Verification Test Suite        ")
    print("====================================================\n")

    # 1. Establish isolated temporary test SQLite database
    test_db_path = "test_incidents.db"
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
        
    print(f"[TEST 1] Setting up isolated database engine: sqlite:///{test_db_path}")
    test_db_url = f"sqlite:///{test_db_path}"
    engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    print("-> SQLite database schemas created successfully.")

    # 2. Seed SOP documents for RAG indexing
    print("\n[TEST 2] Seeding standard operating procedures runbooks...")
    crud.add_kb_doc(
        db=db,
        title="SOP-094: PostgreSQL Connection Pool Exhaustion",
        content="Connection pool capacity drops below 5% or connection slots leak when connections are not released cleanly back to the HikariCP pool. Mitigation: ALTER SYSTEM SET max_connections = 400;",
        source="data/db_connectivity.md"
    )
    # Proactively index doc into Chroma DB if available
    doc_ingestor.ingest_document(
        doc_id="db_connectivity",
        title="SOP-094: PostgreSQL Connection Pool Exhaustion",
        content="Connection pool capacity drops below 5% or connection slots leak when connections are not released cleanly back to the HikariCP pool. Mitigation: ALTER SYSTEM SET max_connections = 400;",
        source="data/db_connectivity.md"
    )
    print("-> SOP documents seeded & indexed.")

    # 3. Simulate User Ingestion Submission
    print("\n[TEST 3] Simulating Incident Ingestion...")
    test_desc = "Critical checkout service timeout failures: Remaining connection slots are reserved on the transactional postgres database replica master."
    test_alarms = "APM checkout latency spike > 5000ms"
    test_env = "prod-us-east-cluster"
    test_severity = "P1"
    
    db_incident = crud.create_incident(
        db=db,
        description=test_desc,
        alarms=test_alarms,
        logs="org.postgresql.util.PSQLException: FATAL: remaining connection slots are reserved",
        env=test_env,
        severity=test_severity
    )
    print(f"-> Ingested incident successfully. Saved with ID: {db_incident.id}")

    # 4. Execute Orchestrator Diagnosis Pipeline
    print("\n[TEST 4] Initiating Orchestrator Pipeline execution...")
    print("Workflow: Ingest -> Retrieve SOP -> Analyze -> Design Runbook -> Escalate -> Checklist")
    
    try:
        state = investigation_orchestrator.run_diagnosis(db, db_incident.id)
        
        print(f"-> Orchestrator workflow complete.")
        print(f"  Classification:  '{state.classification}'")
        print(f"  Confidence:      {state.confidence}%")
        print(f"  Triage Duration: {state.duration}")
        
    except Exception as err:
        print(f"[ERROR] Pipeline execution crashed: {str(err)}")
        db.close()
        sys.exit(1)

    # 5. Verify Database Storage Persistence
    print("\n[TEST 5] Verifying persistent database states...")
    persisted_incident = db.query(models.Incident).filter(models.Incident.id == db_incident.id).first()
    persisted_result = db.query(models.IncidentResult).filter(models.IncidentResult.id == db_incident.id).first()
    
    assert persisted_incident is not None, "Error: Incident was not found in SQLite database!"
    assert persisted_result is not None, "Error: Incident Result was not found in SQLite database!"
    assert persisted_incident.classification == state.classification, "Error: Classification mismatch!"
    
    print("-> Persistence verification checks successful.")
    print(f"  Persisted Incident Description: '{persisted_incident.description[:60]}...'")
    print(f"  Persisted Escalation Team:      '{persisted_result.escalation.get('team')}'")
    print(f"  Persisted Runbook Steps count:  {len(persisted_result.runbook)}")
    
    # Clean up test database connection and file
    db.close()
    try:
        os.remove(test_db_path)
        print("\nCleaned up temporary test database.")
    except Exception as cleanup_err:
        print(f"Warning: Could not remove test database file: {str(cleanup_err)}")

    print("\n====================================================")
    print("     ALL INTEGRATION VERIFICATION TESTS PASSED       ")
    print("====================================================")

if __name__ == "__main__":
    run_integration_test()
