import os
from app.schemas.investigation_state import InvestigationState
from app.logging_config import logger

class InvestigationPlannerAgent:
    def __init__(self):
        self.planner_prompt = ""
        self.escalation_prompt = ""
        self.load_prompt_templates()

    def load_prompt_templates(self):
        try:
            prompts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts")
            
            with open(os.path.join(prompts_dir, "planner_prompt.txt"), "r", encoding="utf-8") as f:
                self.planner_prompt = f.read()
            with open(os.path.join(prompts_dir, "escalation_prompt.txt"), "r", encoding="utf-8") as f:
                self.escalation_prompt = f.read()
                
            logger.info("InvestigationPlannerAgent: Loaded prompts.")
        except Exception as e:
            logger.error(f"InvestigationPlannerAgent: Failed to load prompts: {str(e)}")
            self.planner_prompt = "Design runbook plan..."
            self.escalation_prompt = "Assess escalation matrix..."

    def execute(self, state: InvestigationState) -> InvestigationState:
        # Mandatory logs requirement
        logger.info("[Investigation Planner Agent] Started")
        
        state.console_audit.append("Investigation Planner Agent: Synthesizing SRE recovery plan...")

        classification = state.classification or "General System Outage"

        if classification == "Database Connectivity Failure":
            state.runbook = [
                {"step": "Verify active PostgreSQL database connections count", "detail": "Check if current active connections match max_connections threshold limits."},
                {"step": "Provision additional database capacity slots", "detail": "Execute 'ALTER SYSTEM SET max_connections = 400;' on primary replica master."},
                {"step": "Terminate long-running orphaned transaction queries", "detail": "Identify blocked processes query and run 'pg_terminate_backend(pid)' if necessary."}
            ]
            state.actions = [
                {"title": "Scale Connection Limits", "priority": "Critical", "style": "bg-[#FF5C5C]/10 text-[#FF5C5C] border-[#FF5C5C]/20"},
                {"title": "Purge Idle Threads", "priority": "High", "style": "bg-[#FFC72C]/10 text-[#FFC72C] border-[#FFC72C]/20"}
            ]
            state.escalation = {
                "team": "Data Platform Engineering",
                "level": "L3 Specialist",
                "reason": "Requires master database superuser administrative permissions to alter connections configurations.",
                "group": "On-Call Pod Alpha"
            }
            state.checklist = [
                "PostgreSQL max_connections threshold increased",
                "Application thread-pool connection indicators stabilized",
                "API Checkout Service P99 request latency drops below 200ms"
            ]
        elif classification == "VPN Authentication Failure":
            state.runbook = [
                {"step": "Verify IPSEC tunnel telemetry connection status", "detail": "Check VPN gateway boundary router configurations and connection errors."},
                {"step": "Restart gateway ipsec services", "detail": "Execute systemctl restart ipsec-gateway command locally."},
                {"step": "Verify route entries configurations", "detail": "Verify route maps match VPC boundaries."}
            ]
            state.actions = [
                {"title": "Restart Gateway Router IPSEC", "priority": "Critical", "style": "bg-[#FF5C5C]/10 text-[#FF5C5C] border-[#FF5C5C]/20"},
                {"title": "Reset Boundary Gateway Nodes", "priority": "High", "style": "bg-[#FFC72C]/10 text-[#FFC72C] border-[#FFC72C]/20"}
            ]
            state.escalation = {
                "team": "Core Network Engineering",
                "level": "L3 Specialist",
                "reason": "Requires gateway routing administrator credentials to reset boundary configurations.",
                "group": "Network Infrastructure Pod"
            }
            state.checklist = [
                "VPN tunnel status returns healthy status",
                "Ingress route maps validated and flushed",
                "User gateway authentication request timeouts drops below 1%"
            ]
        elif classification in ["LDAP Bind Failure", "LDAP Certificate Expiry"]:
            state.runbook = [
                {"step": "Verify active directory connections status", "detail": "Test secure LDAPS connections on ports 636/3269."},
                {"step": "Check bind user account status", "detail": "Verify if the LDAP bind service account credentials have expired or are locked in Active Directory."},
                {"step": "Verify LDAP certificate validity", "detail": "Run openssl commands to check trust chains and expiration dates."}
            ]
            state.actions = [
                {"title": "Unlock LDAP Bind Account", "priority": "Critical", "style": "bg-[#FF5C5C]/10 text-[#FF5C5C] border-[#FF5C5C]/20"},
                {"title": "Rotate TLS Certificates", "priority": "High", "style": "bg-[#FFC72C]/10 text-[#FFC72C] border-[#FFC72C]/20"}
            ]
            state.escalation = {
                "team": "Directory Security Operations",
                "level": "L3 Specialist",
                "reason": "Requires active directory domain administrator permissions to unlock accounts or renew TLS certs.",
                "group": "Identity Access Pod"
            }
            state.checklist = [
                "LDAP bind response times drop below 100ms",
                "Authentication errors in microservices logs resolve",
                "Active Directory sync agents report healthy synchronization status"
            ]
        elif classification in ["SSO Login Failure", "Identity Provider Outage"]:
            state.runbook = [
                {"step": "Inspect Okta/Azure AD system logs", "detail": "Check for SAML assertion failures or token signing issues."},
                {"step": "Verify SAML signature validation configuration", "detail": "Verify if signing certificate matches the values mapped on the identity provider console."},
                {"step": "Check Duo API MFA connection health", "detail": "Run connectivity checks to external api.duosecurity.com endpoints."}
            ]
            state.actions = [
                {"title": "Rotate SAML Token Key", "priority": "Critical", "style": "bg-[#FF5C5C]/10 text-[#FF5C5C] border-[#FF5C5C]/20"},
                {"title": "Verify MFA Proxy Daemon", "priority": "High", "style": "bg-[#FFC72C]/10 text-[#FFC72C] border-[#FFC72C]/20"}
            ]
            state.escalation = {
                "team": "Identity & Access Management Team",
                "level": "L3 IAM Specialist",
                "reason": "Requires access to identity provider administration console to map certificates.",
                "group": "IAM Support Pod"
            }
            state.checklist = [
                "Okta login redirect loops resolved",
                "SAML assertions validated successfully on VPN and internal web portals",
                "Duo push notifications delivery success rate returns to normal thresholds"
            ]
        elif classification == "Email Service Failure":
            state.runbook = [
                {"step": "Verify downstream SMTP mail host socket logs", "detail": "Check if logs display socket drops or 535 authentication codes."},
                {"step": "Inspect email delivery queue logs", "detail": "Query email servers delivery queue backlogs status."},
                {"step": "Verify credentials environment variables config", "detail": "Confirm SMTP secrets match current Okta token pairings."}
            ]
            state.actions = [
                {"title": "Update SMTP Secret Auth Tokens", "priority": "Critical", "style": "bg-[#FF5C5C]/10 text-[#FF5C5C] border-[#FF5C5C]/20"},
                {"title": "Flush Email Queue Backlogs", "priority": "Medium", "style": "bg-[#4F8CFF]/10 text-[#4F8CFF] border-[#4F8CFF]/20"}
              ]
            state.escalation = {
                "team": "Directory Security Operations",
                "level": "L2 IAM Engineer",
                "reason": "Requires access to Okta enterprise application credentials settings panels.",
                "group": "Identity Operations Pod"
            }
            state.checklist = [
                "SMTP connection check returns 200 OK success packets",
                "Email backlogs flushed and processed",
                "Verification delivery test registers success"
            ]
        elif classification == "DNS Resolution Failure":
            state.runbook = [
                {"step": "Verify CoreDNS deployment and pod status", "detail": "Run 'kubectl get pods -n kube-system -l k8s-app=kube-dns' to inspect CoreDNS nodes."},
                {"step": "Test DNS lookups from local containers", "detail": "Execute 'nslookup coredns.local' inside microservice containers to verify DNS resolution routing path."},
                {"step": "Check resolv.conf client configuration files", "detail": "Verify if search path or dns nameserver configuration is pointing to correct VPC DNS resolver."}
            ]
            state.actions = [
                {"title": "Scale CoreDNS Replicas", "priority": "Critical", "style": "bg-[#FF5C5C]/10 text-[#FF5C5C] border-[#FF5C5C]/20"},
                {"title": "Restart CoreDNS Pods", "priority": "High", "style": "bg-[#FFC72C]/10 text-[#FFC72C] border-[#FFC72C]/20"}
            ]
            state.escalation = {
                "team": "Infrastructure Platform Pod",
                "level": "L3 Specialist",
                "reason": "Requires Kubernetes cluster admin credentials to scale CoreDNS services.",
                "group": "Cluster Operations Team"
            }
            state.checklist = [
                "CoreDNS query latency drops below 20ms",
                "Container local DNS lookups resolve successfully",
                "VPC DNS hostnames settings verified as enabled"
            ]
        elif classification == "SMTP Authentication Failure":
            state.runbook = [
                {"step": "Verify SMTP authentication logs", "detail": "Check postfix or SendGrid logs for 535 authentication error codes."},
                {"step": "Verify SMTP credentials settings in deployment config", "detail": "Check if secret key or username/password was modified during recent credential rotation."},
                {"step": "Run telnet SMTP connection test", "detail": "Run 'telnet smtp.mail-provider.com 587' to verify connectivity and handshake capability."}
            ]
            state.actions = [
                {"title": "Rotate SMTP Auth Keys", "priority": "Critical", "style": "bg-[#FF5C5C]/10 text-[#FF5C5C] border-[#FF5C5C]/20"},
                {"title": "Flush Postfix Mail Queue", "priority": "Medium", "style": "bg-[#4F8CFF]/10 text-[#4F8CFF] border-[#4F8CFF]/20"}
            ]
            state.escalation = {
                "team": "Directory Security Operations",
                "level": "L2 IAM Engineer",
                "reason": "Requires access to SMTP provider configurations or rotated secrets stores.",
                "group": "Identity Operations Pod"
            }
            state.checklist = [
                "SMTP test authentication succeeds",
                "Outgoing mail delivery queue is empty",
                "Verification delivery test registers success"
            ]
        elif classification == "Unknown Incident":
            state.runbook = [
                {"step": "Collect system log trails", "detail": "Gather diagnostic log files from all failing microservices and nodes."},
                {"step": "Audit central monitoring dashboards", "detail": "Inspect CPU, memory, and database connection metrics to find anomalous components."},
                {"step": "Establish triage channel", "detail": "Open an incident Slack channel and invite on-call engineers."}
            ]
            state.actions = [
                {"title": "Collect Logs and Metrics", "priority": "High", "style": "bg-[#FFC72C]/10 text-[#FFC72C] border-[#FFC72C]/20"},
                {"title": "Open Slack Triage Channel", "priority": "Medium", "style": "bg-[#4F8CFF]/10 text-[#4F8CFF] border-[#4F8CFF]/20"}
            ]
            state.escalation = {
                "team": "General Operations",
                "level": "L1 Support Pod",
                "reason": "Unknown system behavior routing protocol.",
                "group": "SRE Incident Team"
            }
            state.checklist = [
                "Application log files captured",
                "Telemetry dashboards reviewed for bottlenecks",
                "Slack bridge team convened"
            ]
        else: # General System Outage
            state.runbook = [
                {"step": "Trace system stack logs", "detail": "Check application describe and event logs."},
                {"step": "Run process diagnostic checks", "detail": "Check CPU and memory limits settings."}
            ]
            state.actions = [
                {"title": "Verify Deployment Replicas", "priority": "High", "style": "bg-[#FFC72C]/10 text-[#FFC72C] border-[#FFC72C]/20"}
            ]
            state.escalation = {
                "team": "General Operations",
                "level": "L1 Support Pod",
                "reason": "General system triage routing protocol.",
                "group": "SRE Incident Team"
            }
            state.checklist = [
                "Application logs checked",
                "Critical alerts silenced"
            ]

        state.console_audit.append("Investigation Planner Agent: Generated recommended plan runbooks.")
        state.console_audit.append("Investigation Planner Agent: Assigned escalation routing matrix details.")
        
        # Mandatory logs requirement
        logger.info("[Investigation Planner Agent] Completed")
        return state

investigation_planner_agent = InvestigationPlannerAgent()
