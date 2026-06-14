from app.schemas.investigation_state import InvestigationState
from app.logging_config import logger

class RootCauseAgent:
    def __init__(self):
        # Map classification to primary root cause title
        self.root_cause_titles = {
            "VPN Authentication Failure": "IPSEC Tunnel Handshake Timeout",
            "SSO Login Failure": "Identity Provider SAML Certificate Outage",
            "LDAP Bind Failure": "Active Directory LDAP Account Lockout",
            "LDAP Certificate Expiry": "Secure LDAP TLS Certificate Expired",
            "MFA Provider Failure": "Duo MFA API Callback Latency Timeout",
            "Identity Provider Outage": "Okta Enterprise SSO Portal Outage",
            "Database Connectivity Failure": "PostgreSQL Database Engine Connection Refused",
            "Connection Pool Exhaustion": "HikariCP Database Connection Pool Starvation",
            "Database Resource Exhaustion": "RDS Database Instance Disk I/O Saturation",
            "Application Crash": "JVM Heap OutOfMemory Process Termination",
            "API Gateway Failure": "Kong API Gateway Upstream Connection Timeout",
            "Dependency Service Failure": "Downstream Payment API Connection Timeout",
            "Email Service Failure": "Postfix Mail Server Queue Storage Exhausted",
            "SMTP Authentication Failure": "SMTP Gateway Authentication Credentials Mismatch",
            "DNS Resolution Failure": "CoreDNS Service Resolver Timeout",
            "Load Balancer Failure": "Application Load Balancer Target Group Health Check Drop",
            "Network Connectivity Degradation": "WAN Boundary Link Packet Loss",
            "Kubernetes Pod Crashloop": "Kubernetes Pod Liveness Probe Timeout Failure",
            "Container Resource Exhaustion": "Container memory limit exceeded (OOMKilled)",
            "Service Mesh Failure": "Istio Envoy mTLS Handshake Validation Failure",
            "Unknown Incident": "General System Component Failure"
        }

    def execute(self, state: InvestigationState) -> InvestigationState:
        # Mandatory logs requirement
        logger.info("[Root Cause Agent] Started")
        state.console_audit.append("Root Cause Agent: Starting root cause analysis and evidence correlation...")

        classification = state.classification or "Unknown Incident"
        confidence = state.confidence
        
        evidence_summary = state.evidence.get("evidence_summary", {})
        categories = evidence_summary.get("categories", {})

        # Primary Root Cause
        primary_title = self.root_cause_titles.get(classification, "General System Component Failure")
        
        # Supporting Evidence: supporting signals for the selected classification
        supporting = []
        info = categories.get(classification, {})
        if info:
            supporting = info.get("supporting_signals", [])

        # Contradictory Evidence: supporting signals for other categories, or explicit conflicts
        contradictory = []
        conflicts = evidence_summary.get("all_conflicting_signals", [])
        contradictory.extend(conflicts)
        
        for category, info in categories.items():
            if category != classification:
                # Supporting signals for other categories represent contradictory/competing evidence
                for sig in info.get("supporting_signals", []):
                    contradictory.append(f"Matching symptom '{sig}' points to alternative classification {category}.")

        # Determine secondary root causes from candidate list (excluding top candidate)
        candidates = state.evidence.get("candidates", [])
        secondary_root_causes = []
        
        for cand in candidates[1:]:
            cand_name = cand["name"]
            cand_pct = cand["percentage"]
            cand_rc_title = self.root_cause_titles.get(cand_name, "General System Component Failure")
            
            secondary_root_causes.append({
                "title": cand_rc_title,
                "percentage": cand_pct,
                "design": "bg-[#FFC72C]/10 text-[#FFC72C] border-[#FFC72C]/20",
                "strength": "Moderate" if cand_pct >= 30 else "Weak"
            })

        # Save to state
        # Primary Root Cause is saved first in root_causes list
        state.root_causes = [
            {
                "title": primary_title,
                "percentage": confidence,
                "design": "bg-[#FF5C5C]" if confidence >= 50 else "bg-[#9CA3AF]",
                "strength": "Exceptional" if confidence >= 80 else ("High" if confidence >= 50 else "Low")
            }
        ]
        
        # Append secondary root causes
        state.root_causes.extend(secondary_root_causes)

        # Update evidence dict with supporting and contradictory text descriptions
        state.evidence["primary_root_cause"] = primary_title
        state.evidence["supporting_evidence"] = supporting
        state.evidence["contradictory_evidence"] = contradictory

        state.console_audit.append(f"Root Cause Agent: Selected primary root cause: '{primary_title}' (Confidence: {confidence}%).")
        state.console_audit.append(f"Root Cause Agent: Identified {len(secondary_root_causes)} secondary root causes, {len(supporting)} supporting signals, and {len(contradictory)} contradictory signals.")

        # Mandatory logs requirement
        logger.info("[Root Cause Agent] Completed")
        return state

root_cause_agent = RootCauseAgent()
