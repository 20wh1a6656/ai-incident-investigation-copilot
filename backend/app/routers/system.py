from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import database
from app.rag.chroma_manager import chroma_manager
from app.logging_config import logger

router = APIRouter(
    prefix="/system",
    tags=["System"]
)

@router.get("/health")
def healthcheck(db: Session = Depends(database.get_db)):
    # Verify SQLite Connectivity
    db_ok = False
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception as e:
        logger.error(f"System health check failed database query: {str(e)}")

    # Fetch RAG / Chroma metrics
    rag_status = chroma_manager.get_status()

    return {
        "status": "healthy" if db_ok else "degraded",
        "database": {
            "status": "connected" if db_ok else "disconnected",
        },
        "rag": {
            "library_loaded": rag_status["library_available"],
            "chroma_connected": rag_status["connected"],
            "collection_loaded": rag_status["collection_exists"],
            "storage_path": rag_status["storage_path"]
        }
    }
