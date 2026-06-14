import os
from app.schemas.investigation_state import InvestigationState
from app.logging_config import logger

class IncidentAnalysisAgent:
    def __init__(self):
        self.prompt_template = ""
        self.load_prompt_template()

        # Map base filename to classification name
        self.filename_to_class = {
            "vpn_authentication_failure": "VPN Authentication Failure",
            "sso_login_failure": "SSO Login Failure",
            "ldap_bind_failure": "LDAP Bind Failure",
            "ldap_certificate_expiry": "LDAP Certificate Expiry",
            "mfa_provider_failure": "MFA Provider Failure",
            "identity_provider_outage": "Identity Provider Outage",
            "database_connectivity_failure": "Database Connectivity Failure",
            "connection_pool_exhaustion": "Connection Pool Exhaustion",
            "database_resource_exhaustion": "Database Resource Exhaustion",
            "application_crash": "Application Crash",
            "api_gateway_failure": "API Gateway Failure",
            "dependency_service_failure": "Dependency Service Failure",
            "email_service_failure": "Email Service Failure",
            "smtp_authentication_failure": "SMTP Authentication Failure",
            "dns_resolution_failure": "DNS Resolution Failure",
            "load_balancer_failure": "Load Balancer Failure",
            "network_connectivity_degradation": "Network Connectivity Degradation",
            "kubernetes_pod_crashloop": "Kubernetes Pod Crashloop",
            "container_resource_exhaustion": "Container Resource Exhaustion",
            "service_mesh_failure": "Service Mesh Failure"
        }

        # Weighted mapping for SRE signals to distinguish specific vs generic indicators
        self.signal_weights = {
            # Identity / Auth
            "vpn": 5, "ipsec": 5, "anyconnect": 5, "tunnel": 4,
            "sso": 5, "saml": 5, "assertion": 4, "okta": 4,
            "ldap": 5, "bind": 5, "credentials": 4, "active directory": 5, "directory service": 4,
            "certificate": 5, "expiry": 5, "expired": 5, "tls": 4, "ssl": 4, "ldaps": 5,
            "mfa": 5, "duo": 5, "push": 4, "callback": 4,
            "idp": 5, "outage": 3,
            # Database
            "database": 2, "connection": 2, "postgres": 4, "postgresql": 4, "refused": 3, "port 5432": 5,
            "connection pool": 5, "hikaricp": 5, "hikari": 5, "max_connections": 5, "slots": 5,
            "cpu": 3, "memory": 3, "oom": 4, "disk": 4, "iops": 5, "rds": 4,
            # App / K8s
            "oomkilled": 5, "exit code 137": 5, "crashloopbackoff": 5, "liveness": 4, "readiness": 4,
            "gateway": 4, "kong": 5, "nginx": 5, "upstream": 4, "bad gateway": 5,
            "circuit breaker": 5, "payment": 5, "downstream": 4,
            # Network
            "packet loss": 5, "ping": 4, "traceroute": 4, "wan": 4, "degradation": 5,
            "coredns": 5, "port 53": 5, "nslookup": 4, "dig": 4,
            # Email
            "smtp": 3, "email": 2, "mail": 2, "notification": 2, "delivery": 2,
            "authentication": 3, "auth": 3, "535": 5
        }

    def load_prompt_template(self):
        try:
            prompt_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                "prompts", 
                "classification_prompt.txt"
            )
            with open(prompt_path, "r", encoding="utf-8") as f:
                self.prompt_template = f.read()
            logger.info("IncidentAnalysisAgent: Loaded classification prompt template.")
        except Exception as e:
            logger.error(f"IncidentAnalysisAgent: Failed to load classification prompt: {str(e)}")
            self.prompt_template = "Analyze and classify the incident. Ingestion context: {description}"

    def execute(self, state: InvestigationState) -> InvestigationState:
        # Mandatory logs requirement
        logger.info("[Incident Analysis Agent] Started")
        state.console_audit.append("Incident Analysis Agent: Running classification analysis based on evidence correlation...")

        evidence_summary = state.evidence.get("evidence_summary", {})
        categories = evidence_summary.get("categories", {})
        retrieved_chunks = state.evidence.get("retrieved_chunks", [])

        if not categories:
            state.classification = "Unknown Incident"
            state.confidence = 25
            state.evidence["candidates"] = []
            state.evidence["classification_reasoning"] = "No matching SOP chunks retrieved from the knowledge base."
            state.console_audit.append("Incident Analysis Agent: No SOP matches retrieved. Classified as Unknown Incident.")
            logger.info("[Incident Analysis Agent] Completed")
            return state

        # Calculate scores for each category
        scores = {}
        for category, info in categories.items():
            supporting_signals = info["supporting_signals"]
            # Sum weighted signals to favor specific SRE conditions
            supporting_score = sum(self.signal_weights.get(sig, 2) for sig in supporting_signals)
            
            chunks_cnt = info["retrieved_chunks_count"]
            conflict_cnt = len(info["conflicting_signals"])
            
            # Base scoring: 3 points per weighted signal score + 2 points per retrieved chunk
            score = (supporting_score * 3) + (chunks_cnt * 2)
            # Penalize conflicting signals
            if conflict_cnt > 0:
                score -= 6
                
            scores[category] = max(0, score)

        total_score = sum(scores.values())
        
        if total_score == 0:
            state.classification = "Unknown Incident"
            state.confidence = 20
            state.evidence["candidates"] = []
            state.evidence["classification_reasoning"] = "All matched categories scored zero due to lack of supporting signals."
            state.console_audit.append("Incident Analysis Agent: All categories scored zero. Classified as Unknown Incident.")
            logger.info("[Incident Analysis Agent] Completed")
            return state

        # Normalize relative percentage scores
        candidates = []
        for category, score in scores.items():
            relative_pct = int(round((score / total_score) * 100))
            candidates.append({
                "name": category,
                "score": score,
                "percentage": relative_pct
            })

        # Sort candidates by percentage
        candidates.sort(key=lambda x: x["percentage"], reverse=True)
        state.evidence["candidates"] = candidates

        top_cand = candidates[0]
        top_category = top_cand["name"]
        top_pct = top_cand["percentage"]

        # Fetch chunk details for top category
        max_sim = 0
        for chunk in retrieved_chunks:
            source = chunk.get("source", "")
            base_filename = os.path.basename(source).replace(".md", "")
            category_name = self.filename_to_class.get(base_filename, "")
            if category_name == top_category:
                max_sim = max(max_sim, chunk.get("confidence_score", 0))

        info = categories.get(top_category, {})
        supporting_cnt = len(info.get("supporting_signals", []))
        retrieved_cnt = info.get("retrieved_chunks_count", 0)
        conflict_cnt = len(info.get("conflicting_signals", []))
        
        runner_pct = candidates[1]["percentage"] if len(candidates) > 1 else 0

        # Apply new confidence rules
        if max_sim < 40 or supporting_cnt == 0:
            # Low Confidence (0-49%): Weak matches or ambiguous symptoms
            confidence_tier = "Low"
            confidence = 35
        elif conflict_cnt > 0:
            # Medium Confidence (50-79%): Some conflicting evidence
            confidence_tier = "Medium"
            confidence = 58
        elif len(candidates) > 1 and (top_pct - runner_pct) < 15:
            # Medium Confidence (50-79%): Several related categories scoring closely (mixed symptoms)
            confidence_tier = "Medium"
            confidence = 65
        else:
            # High Confidence (80-95%): One dominant category, multiple SOPs, no conflicts
            confidence_tier = "High"
            confidence = min(95, 80 + retrieved_cnt * 2 + supporting_cnt)

        # Unknown Incident detection: if confidence falls below 40%
        if confidence < 40:
            state.classification = "Unknown Incident"
            state.confidence = confidence
            reason = f"Insufficient evidence to determine a primary root cause. Top candidate was {top_category} with only {supporting_cnt} supporting signal(s) and {max_sim}% retrieval match."
            state.evidence["classification_reasoning"] = reason
            state.console_audit.append(f"Incident Analysis Agent: Top candidate {top_category} confidence ({confidence}%) is below 40%. Classified as Unknown Incident.")
        else:
            state.classification = top_category
            state.confidence = confidence
            reason = f"Strong {top_category} evidence present ({supporting_cnt} supporting signals), "
            if len(candidates) > 1:
                reason += f"but {candidates[1]['name']} ({candidates[1]['percentage']}%) indicates possible broader degradation."
            else:
                reason += "with no competing candidate classifications."
            state.evidence["classification_reasoning"] = reason
            state.console_audit.append(f"Incident Analysis Agent: Classified as '{top_category}' (Confidence: {confidence}%). Tier: {confidence_tier}.")

        # Mandatory logs requirement
        logger.info("[Incident Analysis Agent] Completed")
        return state

incident_analysis_agent = IncidentAnalysisAgent()
