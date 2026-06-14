from __future__ import annotations
from sqlalchemy.orm import Session
from app.db import models
from app.logging_config import logger

def create_incident(db: Session, description: str, alarms: str, logs: str, env: str, severity: str) -> models.Incident:
    db_incident = models.Incident(
        description=description,
        alarms=alarms,
        logs=logs,
        env=env,
        severity=severity
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    logger.info(f"Database: Saved raw incident ingestion record with ID {db_incident.id}")
    return db_incident

def get_incident(db: Session, incident_id: str) -> models.Incident | None:
    return db.query(models.Incident).filter(models.Incident.id == incident_id).first()

def get_all_incidents(db: Session, limit: int = 50) -> list[models.Incident]:
    return db.query(models.Incident).order_by(models.Incident.created_at.desc()).limit(limit).all()

def save_incident_result(
    db: Session,
    incident_id: str,
    root_causes: list,
    evidence: dict,
    runbook: list,
    actions: list,
    escalation: dict,
    checklist: list,
    audit: list,
    classification: str,
    confidence: int,
    duration: str
) -> models.IncidentResult:
    # Update incident fields
    db_incident = get_incident(db, incident_id)
    if db_incident:
        db_incident.classification = classification
        db_incident.confidence = confidence
        db_incident.duration = duration
        db.add(db_incident)

    # Save details
    db_result = db.query(models.IncidentResult).filter(models.IncidentResult.id == incident_id).first()
    if not db_result:
        db_result = models.IncidentResult(id=incident_id)

    db_result.root_causes = root_causes
    db_result.evidence = evidence
    db_result.runbook = runbook
    db_result.actions = actions
    db_result.escalation = escalation
    db_result.checklist = checklist
    db_result.audit = audit

    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    logger.info(f"Database: Saved analysis result record linked to Incident {incident_id}")
    return db_result

def get_all_kb_docs(db: Session) -> list[models.KnowledgeBaseDoc]:
    return db.query(models.KnowledgeBaseDoc).all()

def add_kb_doc(db: Session, title: str, content: str, source: str) -> models.KnowledgeBaseDoc:
    db_doc = models.KnowledgeBaseDoc(title=title, content=content, source=source)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    logger.info(f"Database: Added custom knowledge document '{title}' (ID: {db_doc.id})")
    return db_doc
