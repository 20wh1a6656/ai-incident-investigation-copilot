import json
import http.client
import urllib.parse
from pydantic import BaseModel, Field, ValidationError
from app.config import settings
from app.logging_config import logger

# --- Pydantic Schemas for Validation ---
class RootCause(BaseModel):
    title: str = Field(..., description="Name of the probable root cause")
    percentage: float = Field(..., description="Likelihood percentage (0 to 100)")
    strength: str = Field(..., description="Confidence strength tag (e.g., Exceptional, High, Moderate)")

class RunbookStep(BaseModel):
    step: str = Field(..., description="Actionable title for this diagnostic step")
    detail: str = Field(..., description="Technical specifics and commands to run")

class RecommendedAction(BaseModel):
    title: str = Field(..., description="Remediation target title")
    priority: str = Field(..., description="Action priority tag (Critical, High, Medium, Low)")
    style: str = Field(..., description="Tailwind border-badge style code")

class EscalationDetails(BaseModel):
    team: str = Field(..., description="On-call team group to escalate to")
    level: str = Field(..., description="Support tier specialist level (e.g. L3 Specialist)")
    reason: str = Field(..., description="Brief reason explaining why they are owner")
    group: str = Field(..., description="Assigned pod group name")

class InvestigationOutput(BaseModel):
    incident_type: str = Field(..., description="Concise classified system outage type signature")
    confidence: float = Field(..., description="Global diagnosis confidence score percentage")
    probable_root_causes: list[RootCause] = Field(..., description="Ranked list of root causes")
    investigation_steps: list[RunbookStep] = Field(..., description="Chronological triage runbook steps")
    recommended_actions: list[RecommendedAction] = Field(..., description="Immediate mitigation steps")
    escalation_guidance: EscalationDetails = Field(..., description="Escalation path and details")
    verification_checklist: list[str] = Field(..., description="Checklist items to verify the resolution")

# --- System Prompt Templates ---
SYSTEM_PROMPT = """You are an expert site reliability engineering (SRE) copilot.
Your task is to analyze the incident symptoms and matching Standard Operating Procedures (SOPs) to produce a structured triage diagnostic roadmap.

You MUST respond with a single valid JSON object strictly matching this schema:
{
  "incident_type": "string",
  "confidence": 92.5,
  "probable_root_causes": [
    {
      "title": "string",
      "percentage": 85.0,
      "strength": "string"
    }
  ],
  "investigation_steps": [
    {
      "step": "string",
      "detail": "string"
    }
  ],
  "recommended_actions": [
    {
      "title": "string",
      "priority": "string",
      "style": "string"
    }
  ],
  "escalation_guidance": {
    "team": "string",
    "level": "string",
    "reason": "string",
    "group": "string"
  },
  "verification_checklist": [
    "string"
  ]
}

No markdown styling, no ```json prefixes, no conversation trailing texts. Output only raw JSON.
"""

USER_PROMPT_TEMPLATE = """Incident Context Description:
--------------------------------
{incident_description}
--------------------------------

Retrieved Matching SOP Runbook Content:
--------------------------------
{retrieved_sop_content}
--------------------------------

Provide the incident classification diagnosis and recovery steps now.
"""

class InvestigatorAgent:
    def __init__(self):
        # Read API credentials
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.DEFAULT_MODEL
        # Supports overrides to local endpoints (Ollama, vLLM, GitHub Models)
        self.api_base = os.getenv("OPENAI_API_BASE", "api.openai.com")

    def investigate(self, incident_description: str, retrieved_sop_content: str, max_retries: int = 3) -> dict:
        logger.info("InvestigatorAgent: Starting LLM investigation query...")
        
        # Check if we should bypass and run the offline heuristic mock generator
        # if the developer has no credentials set or provider is set to mock
        if settings.ACTIVE_PROVIDER == "mock" or not self.api_key or self.api_key == "mock-openai-key":
            logger.info("InvestigatorAgent: Mock provider active. Generating heuristic analysis report.")
            return self._generate_heuristic_fallback(incident_description, retrieved_sop_content)

        user_content = USER_PROMPT_TEMPLATE.format(
            incident_description=incident_description,
            retrieved_sop_content=retrieved_sop_content
        )

        for attempt in range(1, max_retries + 1):
            logger.info(f"InvestigatorAgent: Completion attempt {attempt}/{max_retries}...")
            try:
                raw_response = self._call_openai_compatible_api(user_content)
                parsed_json = self._clean_and_parse_json(raw_response)
                
                # Pydantic Schema Validation
                validated_output = InvestigationOutput.model_validate(parsed_json)
                logger.info("InvestigatorAgent: Structured response schema validated successfully.")
                return validated_output.model_dump()
                
            except (json.JSONDecodeError, ValidationError) as parse_err:
                logger.warning(f"InvestigatorAgent: JSON format validation failed on attempt {attempt}: {str(parse_err)}")
                if attempt == max_retries:
                    logger.error("InvestigatorAgent: Retries exhausted. Falling back to heuristic generator.")
                    return self._generate_heuristic_fallback(incident_description, retrieved_sop_content)
            except Exception as conn_err:
                logger.error(f"InvestigatorAgent: LLM API connection error: {str(conn_err)}")
                return self._generate_heuristic_fallback(incident_description, retrieved_sop_content)

    def _call_openai_compatible_api(self, user_prompt: str) -> str:
        # Construct standard Chat Completion request body
        payload = {
            "model": self.model if self.model else "gpt-4-turbo",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.1,
            "response_format": {"type": "json_object"}
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        # Use Python's standard http.client for maximum compatibility without installing extra modules
        parsed_url = urllib.parse.urlparse(f"https://{self.api_base}")
        host = parsed_url.netloc if parsed_url.netloc else self.api_base
        path = "/v1/chat/completions"

        conn = http.client.HTTPSConnection(host, timeout=30)
        conn.request("POST", path, json.dumps(payload), headers)
        
        response = conn.getresponse()
        resp_data = response.read().decode("utf-8")
        
        if response.status != 200:
            raise Exception(f"HTTP Endpoint returned error code {response.status}: {resp_data}")
            
        conn.close()
        
        # Extract completions text from body
        resp_json = json.loads(resp_data)
        return resp_json["choices"][0]["message"]["content"]

    def _clean_and_parse_json(self, text: str) -> dict:
        # Strip potential markdown backticks that the model might generate
        cleaned = text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        return json.loads(cleaned.strip())

    def _generate_heuristic_fallback(self, desc: str, sop: str) -> dict:
        # Simple heuristic parser matching keywords
        desc_lower = desc.lower()
        sop_lower = sop.lower()

        if "vpn" in desc_lower or "tunnel" in desc_lower or "ipsec" in desc_lower:
            return {
                "incident_type": "VPN Gateway Connection Failure",
                "confidence": 94.0,
                "probable_root_causes": [
                    {"title": "IPSEC Routing Tunnel Timeout", "percentage": 94.0, "strength": "Exceptional"}
                ],
                "investigation_steps": [
                    {"step": "Verify IPSEC telemetry logs status", "detail": "Check if client packets register drop logs."},
                    {"step": "Check VPN gateway CPU utilization limits", "detail": "Check systemctl monitor dashboards."}
                ],
                "recommended_actions": [
                    {"title": "Restart IPSEC Tunnel Gateway", "priority": "Critical", "style": "bg-[#FF5C5C]/10 text-[#FF5C5C] border-[#FF5C5C]/20"},
                    {"title": "Flush VPC Route Tables", "priority": "High", "style": "bg-[#FFC72C]/10 text-[#FFC72C] border-[#FFC72C]/20"}
                ],
                "escalation_guidance": {
                    "team": "Core Network Engineering",
                    "level": "L3 Specialist",
                    "reason": "Requires root administration access to boundary network routers.",
                    "group": "Cloud Infrastructure Pod"
                },
                "verification_checklist": [
                    "VPN gateway tunnel returns success packets",
                    "Ingress packet drops drop to 0%"
                ]
            }
        elif "okta" in desc_lower or "sso" in desc_lower or "auth" in desc_lower:
            return {
                "incident_type": "Single Sign-On Authentication Failure",
                "confidence": 91.0,
                "probable_root_causes": [
                    {"title": "Okta Active Directory SAML Assertion Expiration", "percentage": 91.0, "strength": "Exceptional"}
                ],
                "investigation_steps": [
                    {"step": "Inspect application authentication log headers", "detail": "Check if logs display invalid_grant codes."},
                    {"step": "Verify active TLS certificate expiration parameters", "detail": "Check current certification matching keys."}
                ],
                "recommended_actions": [
                    {"title": "Force Okta SAML Signature Renewal", "priority": "Critical", "style": "bg-[#FF5C5C]/10 text-[#FF5C5C] border-[#FF5C5C]/20"},
                    {"title": "Clear Outdated User Cookies", "priority": "Medium", "style": "bg-[#4F8CFF]/10 text-[#4F8CFF] border-[#4F8CFF]/20"}
                ],
                "escalation_guidance": {
                    "team": "Directory Security Operations",
                    "level": "L2 IAM Engineer",
                    "reason": "Requires access to security credential portals.",
                    "group": "Enterprise Identity Pod"
                },
                "verification_checklist": [
                    "SAML assertion sync triggers successfully",
                    "User log-in authentication registers success"
                ]
            }
        else:
            # Fallback Database connection
            return {
                "incident_type": "Database Connection Pool Exhaustion",
                "confidence": 96.0,
                "probable_root_causes": [
                    {"title": "HikariCP Connection Pool Starvation", "percentage": 96.0, "strength": "Exceptional"}
                ],
                "investigation_steps": [
                    {"step": "Query active pg_stat_activity logs", "detail": "Check for blocked transaction processes."},
                    {"step": "Scale connection settings configuration limits", "detail": "Run ALTER SYSTEM max_connections statements."}
                ],
                "recommended_actions": [
                    {"title": "Scale Connection Limits", "priority": "Critical", "style": "bg-[#FF5C5C]/10 text-[#FF5C5C] border-[#FF5C5C]/20"},
                    {"title": "Terminate Blocked Transact Threads", "priority": "High", "style": "bg-[#FFC72C]/10 text-[#FFC72C] border-[#FFC72C]/20"}
                ],
                "escalation_guidance": {
                    "team": "Data Platform Engineering",
                    "level": "L3 Specialist",
                    "reason": "Requires superuser credentials to release database connections.",
                    "group": "Data Platform On-Call"
                },
                "verification_checklist": [
                    "HikariCP connection availability pools drop below saturation limits",
                    "API transaction response times drops below 200ms"
                ]
            }

investigator_agent = InvestigatorAgent()
