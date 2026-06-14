from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db import crud, database, models
from app.schemas import incident as schemas
from app.orchestrators.investigation import investigation_orchestrator
from app.exceptions import IncidentNotFoundException, DatabaseException
from app.rag.chroma_manager import chroma_manager
from app.logging_config import logger

router = APIRouter()

@router.post("/investigate", status_code=status.HTTP_200_OK)
def investigate(payload: schemas.IncidentCreate, db: Session = Depends(database.get_db)):
    # 1. Ingest incident metadata
    try:
        db_incident = crud.create_incident(
            db=db,
            description=payload.description,
            alarms=payload.alarms,
            logs=payload.logs,
            env=payload.env,
            severity=payload.severity
        )
    except Exception as e:
        logger.error(f"Failed to ingest incident record: {str(e)}")
        raise DatabaseException("ingest_incident", str(e))
        
    # 2. Run orchestrator diagnosis workflow (calls specialized agents in service layer)
    try:
        state = investigation_orchestrator.run_diagnosis(db, db_incident.id)
        
        # Load persisted detailed results
        db_result = db.query(models.IncidentResult).filter(models.IncidentResult.id == db_incident.id).first()
        
        return {
            "success": True,
            "incident_id": db_incident.id,
            "duration": state.duration,
            "classification": state.classification,
            "confidence": state.confidence,
            "severity": db_incident.severity,
            "results": {
                "root_causes": db_result.root_causes if db_result else [],
                "evidence": db_result.evidence if db_result else {},
                "runbook": db_result.runbook if db_result else [],
                "actions": db_result.actions if db_result else [],
                "escalation": db_result.escalation if db_result else {},
                "checklist": db_result.checklist if db_result else [],
                "audit": db_result.audit if db_result else []
            }
        }
    except Exception as e:
        logger.error(f"Diagnosis pipeline failed for incident {db_incident.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Investigation pipeline failed during execution: {str(e)}"
        )

@router.get("/health", status_code=status.HTTP_200_OK)
def health(db: Session = Depends(database.get_db)):
    db_connected = False
    try:
        db.execute(text("SELECT 1"))
        db_connected = True
    except Exception as e:
        logger.error(f"Healthcheck: DB connectivity check failed: {str(e)}")
        
    rag_status = chroma_manager.get_status()
    
    return {
        "status": "healthy" if db_connected else "degraded",
        "database": {
            "status": "connected" if db_connected else "disconnected"
        },
        "rag": {
            "chroma_connected": rag_status["connected"],
            "library_loaded": rag_status["library_available"]
        }
    }

@router.get("/history", response_model=list[schemas.IncidentResponse], status_code=status.HTTP_200_OK)
def history(db: Session = Depends(database.get_db)):
    try:
        return crud.get_all_incidents(db)
    except Exception as e:
        logger.error(f"Failed to fetch incident history: {str(e)}")
        raise DatabaseException("get_all_incidents", str(e))

@router.get("/investigation/{id}", status_code=status.HTTP_200_OK)
def get_investigation(id: str, db: Session = Depends(database.get_db)):
    db_incident = crud.get_incident(db, id)
    if not db_incident:
        raise IncidentNotFoundException(id)
        
    db_result = db.query(models.IncidentResult).filter(models.IncidentResult.id == id).first()
    
    return {
        "incident": schemas.IncidentResponse.model_validate(db_incident),
        "result": schemas.IncidentResultDetails.model_validate(db_result) if db_result else None
    }
