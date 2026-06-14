import time
from sqlalchemy.orm import Session

from app.schemas.investigation_state import InvestigationState
from app.agents.incident_analysis import incident_analysis_agent
from app.agents.knowledge_retrieval import knowledge_retrieval_agent
from app.agents.evidence_correlation import evidence_correlation_agent
from app.agents.root_cause import root_cause_agent
from app.agents.investigation_planner import investigation_planner_agent
from app.db import crud
from app.logging_config import logger

class InvestigationOrchestrator:
    def run_diagnosis(self, db: Session, incident_id: str) -> InvestigationState:
        # Fetch raw incident context
        db_incident = crud.get_incident(db, incident_id)
        if not db_incident:
            logger.error(f"Orchestrator: Incident {incident_id} not found in database.")
            raise ValueError(f"Incident {incident_id} does not exist.")

        logger.info(f"Orchestrator: Initializing diagnosis pipeline for Incident {incident_id}")
        start_time = time.time()

        # Initialize State Model
        state = InvestigationState(
            incident_id=db_incident.id,
            description=db_incident.description,
            alarms=db_incident.alarms,
            logs_input=db_incident.logs,
            env=db_incident.env,
            severity=db_incident.severity
        )

        state.console_audit.append("Orchestrator: Pipeline initialized. Booting agents...")
        
        try:
            # --- STAGE 1: Knowledge Retrieval Agent (RAG) ---
            state.current_stage = 1
            state.stage_status = "Processing"
            state = knowledge_retrieval_agent.execute(state)
            state.console_audit.append("Orchestrator: Stage 1 Complete - Knowledge Retrieval completed.")

            # --- STAGE 2: Evidence Correlation Agent ---
            state.current_stage = 2
            state.stage_status = "Processing"
            state = evidence_correlation_agent.execute(state)
            state.console_audit.append("Orchestrator: Stage 2 Complete - Evidence Correlation completed.")

            # --- STAGE 3: Classification Agent ---
            state.current_stage = 3
            state.stage_status = "Processing"
            state = incident_analysis_agent.execute(state)
            state.console_audit.append("Orchestrator: Stage 3 Complete - Classification completed.")

            # --- STAGE 4: Root Cause Agent ---
            state.current_stage = 4
            state.stage_status = "Processing"
            state = root_cause_agent.execute(state)
            state.console_audit.append("Orchestrator: Stage 4 Complete - Root Cause Analysis completed.")

            # --- STAGE 5: Investigation Planner Agent ---
            state.current_stage = 5
            state.stage_status = "Processing"
            state = investigation_planner_agent.execute(state)
            state.console_audit.append("Orchestrator: Stage 5 Complete - Plans and escalation guidance designed.")

            # Calculate total duration
            end_time = time.time()
            elapsed = end_time - start_time
            state.duration = f"{elapsed:.2f}s"
            
            state.stage_status = "Done"
            state.console_audit.append("Orchestrator: Pipeline execution finished successfully.")

            # Persist finalized state metrics to SQLite database
            crud.save_incident_result(
                db=db,
                incident_id=state.incident_id,
                root_causes=state.root_causes,
                evidence=state.evidence,
                runbook=state.runbook,
                actions=state.actions,
                escalation=state.escalation,
                checklist=state.checklist,
                audit=state.console_audit,
                classification=state.classification,
                confidence=state.confidence,
                duration=state.duration
            )

            logger.info(f"Orchestrator: Successfully completed diagnostic pipeline in {state.duration}")
            return state

        except Exception as e:
            state.stage_status = "Failed"
            state.error_message = str(e)
            state.console_audit.append(f"Orchestrator Error: Pipeline halted. Reason: {str(e)}")
            logger.critical(f"Orchestrator failed during pipeline run: {str(e)}", exc_info=True)
            
            # Save error trail
            try:
                crud.save_incident_result(
                    db=db,
                    incident_id=state.incident_id,
                    root_causes=[],
                    evidence={},
                    runbook=[],
                    actions=[],
                    escalation={},
                    checklist=[],
                    audit=state.console_audit,
                    classification="Pipeline Execution Failure",
                    confidence=0,
                    duration=f"{(time.time() - start_time):.2f}s"
                )
            except Exception as db_err:
                logger.error(f"Orchestrator: Failed to persist error logs to DB: {str(db_err)}")
                
            raise e

investigation_orchestrator = InvestigationOrchestrator()
