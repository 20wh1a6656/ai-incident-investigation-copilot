import os
import sys

# Ensure backend root is on sys.path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.agents.investigator import investigator_agent

def main():
    print("====================================================")
    print("     Investigator LLM Agent Validation Runner       ")
    print("====================================================\n")

    test_desc = "Outage: Users are unable to login. Authentication requests are timing out, reporting invalid token assertions from Okta security boundaries."
    test_sop = """# SOP-102: Single Sign-On (SSO) Authentication Failures
SSO failures occur when Okta / Active Directory credentials cannot synchronize or when SAML assertions expire.
Mitigation:
- Run okta-admin-sync --force-renew
- Clear session cache files"""

    print("Submitting Outage description & SOP to Agent...")
    try:
        result = investigator_agent.investigate(
            incident_description=test_desc,
            retrieved_sop_content=test_sop
        )
        
        print("\n--- AGENT structured output generated ---")
        print(f"Incident Classification: {result['incident_type']}")
        print(f"AI Global Confidence:    {result['confidence']}%")
        
        print("\nRoot Causes:")
        for rc in result['probable_root_causes']:
            print(f"- {rc['title']} ({rc['percentage']}%) [{rc['strength']}]")
            
        print("\nInvestigation Runbook Steps:")
        for idx, step in enumerate(result['investigation_steps']):
            print(f"{idx+1}. {step['step']}: {step['detail']}")
            
        print("\nRemediation Actions:")
        for act in result['recommended_actions']:
            print(f"- {act['title']} (Priority: {act['priority']})")
            
        print("\nEscalation Target:")
        esc = result['escalation_guidance']
        print(f"- Team: {esc['team']} ({esc['level']})")
        print(f"  Reason: {esc['reason']}")
        print(f"  Pod: {esc['group']}")
        
        print("\nVerification Checklist:")
        for item in result['verification_checklist']:
            print(f"- [ ] {item}")
            
    except Exception as e:
        print(f"[ERROR] Investigation agent execution failed: {str(e)}")

    print("\nVerification execution complete.")

if __name__ == "__main__":
    main()
