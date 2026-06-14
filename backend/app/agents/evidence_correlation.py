import os
from app.schemas.investigation_state import InvestigationState
from app.logging_config import logger

class EvidenceCorrelationAgent:
    def __init__(self):
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

        # SRE diagnostic check terms for each category
        self.category_diagnostics = {
            "VPN Authentication Failure": ["vpn", "tunnel", "ipsec", "anyconnect", "radius"],
            "SSO Login Failure": ["sso", "saml", "assertion", "okta", "single sign-on", "sign-on"],
            "LDAP Bind Failure": ["ldap", "bind", "credentials", "active directory", "directory service"],
            "LDAP Certificate Expiry": ["certificate", "expiry", "expired", "tls", "ssl", "ldaps", "handshake"],
            "MFA Provider Failure": ["mfa", "duo", "push", "callback", "passcode", "multi-factor"],
            "Identity Provider Outage": ["identity provider", "idp", "okta", "azure ad", "adfs", "outage"],
            "Database Connectivity Failure": ["database", "connection", "postgres", "mysql", "sql", "refused", "port 5432"],
            "Connection Pool Exhaustion": ["connection pool", "hikaricp", "hikari", "max_connections", "slots", "exhaustion"],
            "Database Resource Exhaustion": ["cpu", "memory", "oom", "disk", "iops", "latency", "rds"],
            "Application Crash": ["oomkilled", "exit code 137", "crashloopbackoff", "liveness", "readiness", "crash"],
            "API Gateway Failure": ["gateway", "kong", "nginx", "upstream", "timeout", "bad gateway"],
            "Dependency Service Failure": ["circuit breaker", "payment", "downstream", "dependency", "api"],
            "Email Service Failure": ["email", "mail", "notification", "smtp", "postfix", "delivery"],
            "SMTP Authentication Failure": ["smtp", "authentication", "auth", "credentials", "535"],
            "DNS Resolution Failure": ["dns", "resolution", "lookup", "nxdomain", "servfail", "nslookup", "dig", "coredns", "port 53"],
            "Load Balancer Failure": ["load balancer", "healthyhostcount", "target group", "cname", "unhealthy"],
            "Network Connectivity Degradation": ["packet loss", "latency", "ping", "traceroute", "wan", "degradation"],
            "Kubernetes Pod Crashloop": ["pod", "crashloop", "kubectl", "describe", "probe", "readiness"],
            "Container Resource Exhaustion": ["container", "oom", "cpu", "memory", "throttling", "limit"],
            "Service Mesh Failure": ["mesh", "sidecar", "proxy", "envoy", "istio", "mtls"]
        }

    def execute(self, state: InvestigationState) -> InvestigationState:
        # Mandatory logs requirement
        logger.info("[Evidence Correlation Agent] Started")
        state.console_audit.append("Evidence Correlation Agent: Grouping retrieved SOP chunks and mapping diagnostic signals...")

        retrieved_chunks = state.evidence.get("retrieved_chunks", [])
        
        desc_lower = state.description.lower()
        logs_lower = (state.logs_input or "").lower()
        alarms_lower = (state.alarms or "").lower()
        incident_context = f"{desc_lower} {logs_lower} {alarms_lower}"

        categories_summary = {}
        all_supporting = set()
        all_conflicting = set()

        for chunk in retrieved_chunks:
            source = chunk.get("source", "")
            base_filename = os.path.basename(source).replace(".md", "")
            category = self.filename_to_class.get(base_filename, "General System Outage")
            
            if category not in categories_summary:
                categories_summary[category] = {
                    "retrieved_chunks_count": 0,
                    "supporting_signals": [],
                    "missing_evidence": [],
                    "conflicting_signals": []
                }
                
            categories_summary[category]["retrieved_chunks_count"] += 1

        # Analyze diagnostics per category
        for category, info in categories_summary.items():
            diag_terms = self.category_diagnostics.get(category, [])
            supporting = []
            missing = []
            
            for term in diag_terms:
                if term in incident_context:
                    supporting.append(term)
                    all_supporting.add(term)
                else:
                    missing.append(term)
                    
            info["supporting_signals"] = supporting
            info["missing_evidence"] = missing
            
            # If a category was retrieved by RAG but has 0 supporting terms in incident context,
            # it represents conflicting/irrelevant evidence
            if len(supporting) == 0:
                conflict_msg = f"Retrieved {category} SOP, but no diagnostic signals matched incident context."
                info["conflicting_signals"].append(conflict_msg)
                all_conflicting.add(conflict_msg)

        # Build evidence summary dictionary
        evidence_summary = {
            "categories": categories_summary,
            "all_supporting_signals": list(all_supporting),
            "all_conflicting_signals": list(all_conflicting)
        }
        
        state.evidence["evidence_summary"] = evidence_summary
        
        state.console_audit.append(f"Evidence Correlation Agent: Grouped evidence into {len(categories_summary)} categories.")
        state.console_audit.append(f"Evidence Correlation Agent: Detected {len(all_supporting)} supporting signals and {len(all_conflicting)} conflicting signals.")

        # Mandatory logs requirement
        logger.info("[Evidence Correlation Agent] Completed")
        return state

evidence_correlation_agent = EvidenceCorrelationAgent()
