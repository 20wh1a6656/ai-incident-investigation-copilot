import datetime
import uuid
from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String, primary_key=True, default=generate_uuid)
    description = Column(Text, nullable=False)
    alarms = Column(String, nullable=True)
    logs = Column(Text, nullable=True)
    env = Column(String, nullable=True)
    severity = Column(String, nullable=False, default="P3")
    classification = Column(String, nullable=True)
    confidence = Column(Integer, nullable=True)
    duration = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    result = relationship("IncidentResult", back_populates="incident", uselist=False, cascade="all, delete-orphan")

class IncidentResult(Base):
    __tablename__ = "incident_results"

    id = Column(String, ForeignKey("incidents.id", ondelete="CASCADE"), primary_key=True)
    root_causes = Column(JSON, nullable=True)   # Array of root cause objects
    evidence = Column(JSON, nullable=True)     # Evidence context mapping
    runbook = Column(JSON, nullable=True)      # Recommended plan steps
    actions = Column(JSON, nullable=True)      # Immediate remediation targets
    escalation = Column(JSON, nullable=True)   # Teams and routing
    checklist = Column(JSON, nullable=True)    # Post-verification checklist array
    audit = Column(JSON, nullable=True)        # Console audit timeline traces

    # Relationships
    incident = relationship("Incident", back_populates="result")

class KnowledgeBaseDoc(Base):
    __tablename__ = "knowledge_base_docs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
