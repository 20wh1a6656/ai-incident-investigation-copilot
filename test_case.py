import sys
import os

# Ensure backend root is on sys.path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.schemas.investigation_state import InvestigationState
from app.agents.incident_analysis import incident_analysis_agent
from app.agents.knowledge_retrieval import knowledge_retrieval_agent
from app.agents.investigation_planner import investigation_planner_agent

def main():
    desc = """Users cannot login to VPN.
SSO portal unavailable.
Email notifications failing.
Multiple services reporting authentication errors.
LDAP bind failures observed."""

    state = InvestigationState(
        incident_id="debug-incident-123",
        description=desc,
        alarms="Multiple Auth Errors",
        logs_input="LDAP bind failures observed"
    )

    print("Running Incident Analysis Agent...")
    state = incident_analysis_agent.execute(state)
    print(f"Classification: '{state.classification}' | Confidence: {state.confidence}%\n")

    print("Running Knowledge Retrieval Agent...")
    state = knowledge_retrieval_agent.execute(state)
    print(f"Evidence retrieved: {state.evidence}\n")

    print("Running Investigation Planner Agent...")
    state = investigation_planner_agent.execute(state)
    print(f"Planner output runbook: {state.runbook}\n")
    print(f"Planner output actions: {state.actions}\n")
    print(f"Planner output escalation: {state.escalation}\n")
    print(f"Planner output checklist: {state.checklist}\n")

if __name__ == "__main__":
    main()
