from __future__ import annotations
from pydantic import BaseModel, Field

class InvestigationState(BaseModel):
    incident_id: str
    description: str
    alarms: str | None = None
    logs_input: str | None = None
    env: str | None = None
    severity: str = "P3"
    
    # State tracking variables
    current_stage: int = Field(1, description="Current execution stage (1-5)")
    stage_status: str = Field("Pending", description="Status of current stage (Pending, Processing, Done, Failed)")
    console_audit: list[str] = Field(default_factory=list, description="Historical list of console audit steps")
    
    # Pipeline Intermediate outputs
    classification: str | None = None
    confidence: int = 0
    duration: str = "0.0s"
    
    root_causes: list[dict] = Field(default_factory=list)
    evidence: dict = Field(default_factory=dict)
    runbook: list[dict] = Field(default_factory=list)
    actions: list[dict] = Field(default_factory=list)
    escalation: dict = Field(default_factory=dict)
    checklist: list[str] = Field(default_factory=list)
    
    # Error states
    error_message: str | None = None
