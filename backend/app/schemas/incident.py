from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field

class IncidentCreate(BaseModel):
    description: str = Field(..., min_length=5, description="Core outage telemetry / context details")
    alarms: str | None = Field(None, description="Active alarms monitoring tag")
    logs: str | None = Field(None, description="Diagnostic logs dump / stack trace")
    env: str | None = Field(None, description="Environment identification descriptor")
    severity: str = Field("P3", description="Blast severity indicator (P1, P2, P3, P4)")

class IncidentResponse(BaseModel):
    id: str
    description: str
    alarms: str | None
    logs: str | None
    env: str | None
    severity: str
    classification: str | None
    confidence: int | None
    duration: str | None
    created_at: datetime

    class Config:
        from_attributes = True

class IncidentResultDetails(BaseModel):
    root_causes: list | None
    evidence: dict | None
    runbook: list | None
    actions: list | None
    escalation: dict | None
    checklist: list | None
    audit: list | None

    class Config:
        from_attributes = True

class IncidentDetailResponse(BaseModel):
    incident: IncidentResponse
    result: IncidentResultDetails | None

class KBDocCreate(BaseModel):
    title: str
    content: str
    source: str

class KBDocResponse(BaseModel):
    id: int
    title: str
    content: str
    source: str
    created_at: datetime

    class Config:
        from_attributes = True
