from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.logging_config import logger
from app.exceptions import CopilotException, copilot_exception_handler, global_exception_handler
from app.routers import api, incidents, system
from app.db.database import engine, Base, SessionLocal
from app.db import crud

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQL database tables
    logger.info("Initializing SQLite database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("SQLite tables created successfully.")

    # Seed default knowledge base runbook documents for fallback RAG
    db = SessionLocal()
    try:
        existing_docs = crud.get_all_kb_docs(db)
        if not existing_docs:
            logger.info("Seeding initial standard operating procedures into Knowledge Base...")
            crud.add_kb_doc(
                db=db,
                title="SOP-094: PostgreSQL Scale Limits",
                content="When remaining database connection pool capacity drops below 5% or connection slots leak, increase PostgreSQL max_connections setting or adjust connection timeouts. Standard limits require pool throttling and scale limits configured.",
                source="Confluence Wiki Runbooks"
            )
            crud.add_kb_doc(
                db=db,
                title="SOP-112: Redis Cache Configuration Guide",
                content="Active eviction issues occur under volatile-lru constraints when memory utilization exceeds 90%. Scale cluster keys, clean orphaned slots, and verify eviction policies. Flush idle keys if memory leaks persist.",
                source="Architecture Playbook Docs"
            )
            crud.add_kb_doc(
                db=db,
                title="SOP-057: CoreDNS Resolver Debugging",
                content="Downstream timeouts and network resolution failures occur when CoreDNS cluster nodes drop traffic under heavy load. Verify endpoint routes, restart dns pods, and verify resolv.conf configurations.",
                source="Kubernetes On-Call Guide"
            )
            logger.info("Knowledge base seeding completed.")
    except Exception as e:
        logger.error(f"Error seeding database records during bootstrap: {str(e)}")
    finally:
        db.close()
        
    yield
    logger.info("Shutting down AI Incident Investigation Copilot backend API service.")

# Instantiate FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise automated triage pipelines for system outages, alert traces, and runbooks.",
    version="1.0.0",
    lifespan=lifespan
)

# Apply CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers mapping
app.add_exception_handler(CopilotException, copilot_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Include Router (prefixed and root versions for path flexibility)
app.include_router(api.router, prefix="/api")
app.include_router(incidents.router, prefix="/api")
app.include_router(system.router, prefix="/api")

app.include_router(api.router)
app.include_router(incidents.router)
app.include_router(system.router)

@app.get("/")
def read_root():
    return {
        "app": settings.PROJECT_NAME,
        "version": "1.0.0",
        "documentation": "/docs"
    }
