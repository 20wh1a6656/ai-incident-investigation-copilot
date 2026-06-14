from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import crud, database, models
from app.schemas import incident as schemas
from app.orchestrators.investigation import investigation_orchestrator
from app.exceptions import IncidentNotFoundException, DatabaseException
from app.logging_config import logger

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)

@router.post("/ingest", response_model=schemas.IncidentResponse, status_code=status.HTTP_201_CREATED)
def ingest_incident(payload: schemas.IncidentCreate, db: Session = Depends(database.get_db)):
    try:
        db_incident = crud.create_incident(
            db=db,
            description=payload.description,
            alarms=payload.alarms,
            logs=payload.logs,
            env=payload.env,
            severity=payload.severity
        )
        return db_incident
    except Exception as e:
        logger.error(f"Router: Failed to ingest incident: {str(e)}")
        raise DatabaseException("ingest_incident", str(e))

@router.post("/{incident_id}/diagnose", status_code=status.HTTP_200_OK)
def diagnose_incident(incident_id: str, db: Session = Depends(database.get_db)):
    db_incident = crud.get_incident(db, incident_id)
    if not db_incident:
        raise IncidentNotFoundException(incident_id)
        
    try:
        # Trigger orchestrator
        state = investigation_orchestrator.run_diagnosis(db, incident_id)
        return {
            "success": True,
            "incident_id": incident_id,
            "duration": state.duration,
            "classification": state.classification,
            "confidence": state.confidence,
            "results": {
                "root_causes": state.root_causes,
                "evidence": state.evidence,
                "runbook": state.runbook,
                "actions": state.actions,
                "escalation": state.escalation,
                "checklist": state.checklist,
                "audit": state.console_audit
            }
        }
    except Exception as e:
        logger.error(f"Router: Pipeline failure on diagnosis for {incident_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Triage pipeline failed: {str(e)}"
        )

@router.get("/history", response_model=list[schemas.IncidentResponse])
def get_incident_history(limit: int = 50, db: Session = Depends(database.get_db)):
    try:
        return crud.get_all_incidents(db, limit=limit)
    except Exception as e:
        logger.error(f"Router: History query failed: {str(e)}")
        raise DatabaseException("get_incident_history", str(e))

@router.get("/{incident_id}", response_model=schemas.IncidentDetailResponse)
def get_incident_details(incident_id: str, db: Session = Depends(database.get_db)):
    db_incident = crud.get_incident(db, incident_id)
    if not db_incident:
        raise IncidentNotFoundException(incident_id)

    db_result = db.query(models.IncidentResult).filter(models.IncidentResult.id == incident_id).first()
    
    return schemas.IncidentDetailResponse(
        incident=schemas.IncidentResponse.model_validate(db_incident),
        result=schemas.IncidentResultDetails.model_validate(db_result) if db_result else None
    )

@router.post("/kb", response_model=schemas.KBDocResponse, status_code=status.HTTP_201_CREATED)
def add_knowledge_base_document(payload: schemas.KBDocCreate, db: Session = Depends(database.get_db)):
    try:
        # Add to database
        db_doc = crud.add_kb_doc(
            db=db,
            title=payload.title,
            content=payload.content,
            source=payload.source
        )
        
        # Proactively index doc into Chroma via RAG layer
        from app.rag.ingest import doc_ingestor
        doc_ingestor.ingest_document(
            doc_id=f"kb-doc-{db_doc.id}",
            title=db_doc.title,
            content=db_doc.content,
            source=db_doc.source
        )
        
        return db_doc
    except Exception as e:
        logger.error(f"Router: Failed to ingest KB document: {str(e)}")
        raise DatabaseException("add_knowledge_base_document", str(e))

@router.get("/kb", response_model=list[schemas.KBDocResponse])
def list_knowledge_base_documents(db: Session = Depends(database.get_db)):
    try:
        return crud.get_all_kb_docs(db)
    except Exception as e:
        logger.error(f"Router: KB list query failed: {str(e)}")
        raise DatabaseException("list_knowledge_base_documents", str(e))
