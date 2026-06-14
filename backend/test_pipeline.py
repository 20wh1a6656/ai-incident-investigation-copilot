import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure backend root is on sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.db.database import Base
from app.db import crud, models
from app.orchestrators.investigation import investigation_orchestrator

@pytest.fixture(scope="module")
def test_db():
    # Setup test database
    db_path = "pipeline_test.db"
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception:
            pass

    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    yield db
    
    # Cleanup after all tests
    db.close()
    try:
        os.remove(db_path)
    except Exception:
        pass

def test_vpn_authentication_failure(test_db):
    desc = "Users report Cisco AnyConnect VPN client connection timeout at IPSEC phase-2 handshake and remote access gateway failures."
    incident = crud.create_incident(
        db=test_db,
        description=desc,
        alarms="VPN tunnel negotiation timeout",
        logs="IPSEC phase-2 handshake timeout",
        env="prod-network",
        severity="P2"
    )
    state = investigation_orchestrator.run_diagnosis(test_db, incident.id)
    
    assert state.classification == "VPN Authentication Failure"
    assert state.confidence >= 80  # High confidence
    assert state.root_causes[0]["title"] == "IPSEC Tunnel Handshake Timeout"
    assert len(state.evidence["supporting_evidence"]) > 0
    assert "vpn" in state.evidence["supporting_evidence"]

def test_ldap_bind_failure(test_db):
    desc = "Active directory domain controller logs report LDAP bind failures and invalid credentials code 49 when authenticating SRE logins."
    incident = crud.create_incident(
        db=test_db,
        description=desc,
        alarms="LDAP lookup timeout",
        logs="ldap_bind: authentication failure, error code 49",
        env="prod-auth-infra",
        severity="P1"
    )
    state = investigation_orchestrator.run_diagnosis(test_db, incident.id)
    
    assert state.classification == "LDAP Bind Failure"
    assert state.confidence >= 80  # High confidence
    assert state.root_causes[0]["title"] == "Active Directory LDAP Account Lockout"

def test_smtp_authentication_failure(test_db):
    desc = "Email notification delivery failing. Mail server logs show SMTP authentication failure code 535 credentials mismatch."
    incident = crud.create_incident(
        db=test_db,
        description=desc,
        alarms="Mail delivery queue backlog",
        logs="smtp_auth: 535 Authentication failed",
        env="prod-mail",
        severity="P3"
    )
    state = investigation_orchestrator.run_diagnosis(test_db, incident.id)
    
    assert state.classification == "SMTP Authentication Failure"
    assert state.confidence >= 80  # High confidence
    assert state.root_causes[0]["title"] == "SMTP Gateway Authentication Credentials Mismatch"

def test_dns_resolution_failure(test_db):
    desc = "CoreDNS resolver timeout and nxdomain errors observed. Internal hostname lookup failures for cluster services."
    incident = crud.create_incident(
        db=test_db,
        description=desc,
        alarms="Kubernetes cluster DNS latency spike",
        logs="CoreDNS: NXDOMAIN for internal gateway addresses",
        env="prod-k8s",
        severity="P1"
    )
    state = investigation_orchestrator.run_diagnosis(test_db, incident.id)
    
    assert state.classification == "DNS Resolution Failure"
    assert state.confidence >= 80  # High confidence
    assert state.root_causes[0]["title"] == "CoreDNS Service Resolver Timeout"

def test_database_connection_pool_exhaustion(test_db):
    desc = "HikariCP database connection pool exhaustion detected. PSQLException: remaining connection slots are reserved on postgres master."
    incident = crud.create_incident(
        db=test_db,
        description=desc,
        alarms="Database pool acquisition timeout",
        logs="FATAL: remaining connection slots are reserved",
        env="prod-db",
        severity="P1"
    )
    state = investigation_orchestrator.run_diagnosis(test_db, incident.id)
    
    assert state.classification == "Connection Pool Exhaustion"
    assert state.confidence >= 80  # High confidence
    assert state.root_causes[0]["title"] == "HikariCP Database Connection Pool Starvation"

def test_multi_symptom_identity_incident(test_db):
    desc = """Users cannot login to VPN.
SSO portal unavailable.
Email notifications failing.
Multiple services reporting authentication errors.
LDAP bind failures observed."""
    incident = crud.create_incident(
        db=test_db,
        description=desc,
        alarms="SSO portal HTTP 503, LDAP timeouts",
        logs="ldap_bind error: code 49; smtp credentials mismatch",
        env="prod-infra",
        severity="P1"
    )
    state = investigation_orchestrator.run_diagnosis(test_db, incident.id)
    
    # Confirms multi-symptom maps to LDAP Bind Failure but with lower/medium confidence due to mixed symptoms
    assert state.classification == "LDAP Bind Failure"
    assert 50 <= state.confidence <= 79  # Medium confidence tier
    assert len(state.evidence["candidates"]) >= 2
    assert any(c["name"] == "SSO Login Failure" for c in state.evidence["candidates"])
    assert len(state.evidence["contradictory_evidence"]) > 0

def test_ambiguous_incident(test_db):
    desc = "Some systems are behaving strangely. There is a general slowness in checkout gateways and user logins."
    incident = crud.create_incident(
        db=test_db,
        description=desc,
        alarms="General gateway latency alerts",
        logs="",
        env="prod-gateway",
        severity="P3"
    )
    state = investigation_orchestrator.run_diagnosis(test_db, incident.id)
    
    # Ambiguous symptoms should map to Unknown Incident
    assert state.classification == "Unknown Incident"
    assert state.confidence < 40  # Low confidence
    assert any("Unknown Incident" in line for line in state.console_audit)

def test_unknown_incident(test_db):
    desc = "Unknown critical failure occurred on internal boundary routers during backup replication loops. Logs show generic EOF errors."
    incident = crud.create_incident(
        db=test_db,
        description=desc,
        alarms="Boundary link down",
        logs="EOF error on tunnel interface",
        env="prod-edge",
        severity="P1"
    )
    state = investigation_orchestrator.run_diagnosis(test_db, incident.id)
    
    assert state.classification == "Unknown Incident"
    assert state.confidence < 40  # Low confidence
    assert len(state.runbook) == 3
    assert state.runbook[0]["step"] == "Collect system log trails"
