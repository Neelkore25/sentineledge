import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# Fix AI investigator service
write_file("apps/api/services/ai_investigator.py", """import os
import json
from typing import Optional
import httpx
from apps.api.core.config import settings

class AIInvestigatorService:
    \"\"\"
    Evidence-grounded AI investigator service.
    Strictly accepts only structured evidence packages (telemetry IDs, baseline metrics, asset context).
    Provides deterministic local fallback when no external API key is present.
    \"\"\"

    @staticmethod
    def generate_deterministic_analysis(evidence_package: dict) -> dict:
        incident = evidence_package.get("incident", {})
        events = evidence_package.get("events", [])
        user_baseline = evidence_package.get("user_baseline", {})
        asset = evidence_package.get("asset", {})
        risk = evidence_package.get("risk_breakdown", {})
        recovery = evidence_package.get("recovery_context", {})

        event_ids = [e.get("id") for e in events if e.get("id")]
        event_types = list(set(e.get("event_type") for e in events if e.get("event_type")))
        unique_ips = list(set(e.get("source_ip") for e in events if e.get("source_ip")))
        username = incident.get("affected_user") or "unknown_user"
        asset_name = incident.get("affected_asset") or (asset.get("asset_name") if asset else "Critical Infrastructure")

        # Build grounded evidence bullet list citing exact event IDs
        evidence_citations = []
        if any("LOGIN_FAILED" in str(et) for et in event_types):
            failed_evs = [e["id"] for e in events if "LOGIN_FAILED" in str(e.get("event_type", ""))]
            evidence_citations.append(f"Repeated authentication failures observed across event IDs: {', '.join(failed_evs[:4])}.")
        if any("LOGIN_SUCCESS" in str(et) for et in event_types):
            succ_evs = [e["id"] for e in events if "LOGIN_SUCCESS" in str(e.get("event_type", ""))]
            evidence_citations.append(f"Successful session authentication established in event ID: {', '.join(succ_evs)}.")
        if any("PRIVILEGE" in str(et) or "ADMIN" in str(et) for et in event_types):
            priv_evs = [e["id"] for e in events if "PRIVILEGE" in str(e.get("event_type", "")) or "ADMIN" in str(e.get("event_type", ""))]
            evidence_citations.append(f"Privilege modification or administrative elevation detected in: {', '.join(priv_evs)}.")
        if any("DOWNLOAD" in str(e.get("event_type", "")) or e.get("bytes_transferred", 0) > 50_000_000 for e in events):
            exfil_evs = [e["id"] for e in events if e.get("bytes_transferred", 0) > 50_000_000 or "DOWNLOAD" in str(e.get("event_type", ""))]
            evidence_citations.append(f"Anomalous high-volume outbound data transfer detected in: {', '.join(exfil_evs)}.")

        if not evidence_citations:
            evidence_citations = [f"Correlated {len(events)} telemetry events referencing IDs: {', '.join(event_ids[:5])}."]

        primary_hypothesis = f"Correlated activity indicates anomalous unauthorized access pattern targeting '{asset_name}' utilizing identity '{username}' from external source IP(s) {unique_ips}."
        alternative_explanation = f"Legitimate administrative operation conducted outside standard working hours via VPN or authorized external consultant."
        missing_evidence = f"Endpoint EDR process trees and multi-factor authentication challenge audit logs from identity provider are required to confirm host execution."
        
        recommended_actions = [
            f"Simulate session revocation and temporary credential lock for user '{username}'.",
            f"Inspect firewall logs for persistent egress connections to IP(s) {unique_ips}.",
            f"Verify backup immutability on asset '{asset_name}' (Current RPO Gap: {recovery.get('rpo_gap_hours', 0.0)}h)."
        ]

        summary = f"Automated evidence correlation assembled {len(events)} security events against {asset_name}. Risk model scored technical and business impact at {risk.get('composite_risk_score', incident.get('risk_score', 75.0))}/100 ({risk.get('severity_band', 'HIGH')})."

        return {
            "mode": "Local Research Assistant (Deterministic Evidence Grounded)",
            "summary": summary,
            "primary_hypothesis": primary_hypothesis,
            "alternative_explanation": alternative_explanation,
            "evidence_citations": evidence_citations,
            "missing_evidence": missing_evidence,
            "confidence_score": 0.88,
            "recommended_actions": recommended_actions,
            "model_used": "SentinelEdge-Deterministic-Engine-v1"
        }

    @classmethod
    async def investigate_incident(cls, evidence_package: dict) -> dict:
        provider = settings.AI_PROVIDER.lower()
        api_key = settings.AI_API_KEY

        if provider in ("openai", "gemini", "anthropic") and api_key:
            try:
                system_prompt = (
                    "You are the SentinelEdge Incident Investigation Assistant. "
                    "You MUST use ONLY the supplied evidence package. "
                    "NEVER invent events, users, IP addresses, timestamps, or system actions. "
                    "Explicitly cite supplied event IDs. "
                    "Separate observed facts from hypotheses. "
                    "Return valid JSON matching the requested schema."
                )
                user_content = json.dumps(evidence_package)

                if provider == "openai":
                    async with httpx.AsyncClient(timeout=15.0) as client:
                        prompt_msg = "Investigate this evidence package and return JSON with summary, primary_hypothesis, alternative_explanation, evidence_citations (list), missing_evidence, confidence_score (float 0-1), recommended_actions (list):\n" + user_content
                        resp = await client.post(
                            "https://api.openai.com/v1/chat/completions",
                            headers={"Authorization": f"Bearer {api_key}"},
                            json={
                                "model": settings.AI_MODEL or "gpt-4o-mini",
                                "messages": [
                                    {"role": "system", "content": system_prompt},
                                    {"role": "user", "content": prompt_msg}
                                ],
                                "response_format": {"type": "json_object"}
                            }
                        )
                        if resp.status_code == 200:
                            data = resp.json()
                            content = data["choices"][0]["message"]["content"]
                            parsed = json.loads(content)
                            parsed["mode"] = f"Cloud AI Provider ({provider})"
                            parsed["model_used"] = settings.AI_MODEL
                            return parsed
            except Exception as e:
                print(f"External AI Provider error: {e}. Falling back to deterministic analysis.")

        return cls.generate_deterministic_analysis(evidence_package)
""")

# Fix Pydantic v2 ConfigDict in schemas
write_file("apps/api/schemas/event.py", """from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Any

class SecurityEventBase(BaseModel):
    source: str
    user_id: Optional[str] = None
    asset_id: Optional[str] = None
    source_ip: Optional[str] = None
    event_type: str
    action: Optional[str] = None
    status: str
    endpoint: Optional[str] = None
    device_id: Optional[str] = None
    location: Optional[str] = None
    bytes_transferred: int = 0
    event_metadata: dict[str, Any] = Field(default_factory=dict)

class SecurityEventCreate(SecurityEventBase):
    id: Optional[str] = None
    timestamp: Optional[datetime] = None

class SecurityEventResponse(SecurityEventBase):
    id: str
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
""")

write_file("apps/api/schemas/incident.py", """from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Any

class RiskBreakdownSchema(BaseModel):
    r_rule: float = Field(description="Normalized Rule Severity Sub-score [0, 100]")
    s_behavior: float = Field(description="Normalized Behavioral Deviation Sub-score [0, 100]")
    c_correlation: float = Field(description="Normalized Correlation Group Sub-score [0, 100]")
    a_criticality: float = Field(description="Normalized Asset Criticality Sub-score [0, 100]")
    b_impact: float = Field(description="Normalized Business Impact Sub-score [0, 100]")
    weights: dict[str, float] = Field(description="Weights applied to each sub-score")
    weighted_contributions: dict[str, float] = Field(description="Weighted points contributed")
    composite_risk_score: float = Field(description="Total composite risk score [0, 100]")
    severity_band: str = Field(description="LOW, MEDIUM, HIGH, CRITICAL")
    formula: str = Field(description="Human-readable formula string")

class IncidentBase(BaseModel):
    title: str
    description: str
    severity: str
    risk_score: float
    status: str = "OPEN"
    affected_asset: Optional[str] = None
    affected_user: Optional[str] = None
    attack_category: str
    business_impact: str = "MEDIUM"
    confidence: float = 0.85
    correlation_group: str
    event_ids: list[str] = Field(default_factory=list)
    risk_breakdown: Optional[dict[str, Any]] = Field(default_factory=dict)
    ai_summary: Optional[str] = None
    ai_hypothesis: Optional[str] = None
    ai_alternative: Optional[str] = None
    ai_missing_evidence: Optional[str] = None
    recommended_action: Optional[str] = None

class IncidentCreate(IncidentBase):
    id: Optional[str] = None
    detected_at: Optional[datetime] = None
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None

class IncidentResponse(IncidentBase):
    id: str
    detected_at: datetime
    first_seen: datetime
    last_seen: datetime
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
""")

write_file("apps/api/schemas/asset.py", """from pydantic import BaseModel, ConfigDict
from typing import Optional

class AssetBase(BaseModel):
    asset_name: str
    asset_type: str
    criticality: str
    owner: str
    business_function: str
    data_sensitivity: str
    estimated_downtime_cost_per_hour: float = 1000.0
    user_blast_radius: int = 50

class AssetCreate(AssetBase):
    id: str

class AssetResponse(AssetBase):
    id: str
    model_config = ConfigDict(from_attributes=True)
""")

write_file("apps/api/schemas/user.py", """from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserEntityBase(BaseModel):
    username: str
    full_name: str
    role: str
    typical_login_start_hour: int = 9
    typical_login_end_hour: int = 18
    typical_locations: list[str] = ["Mumbai", "Bengaluru"]
    typical_devices: list[str] = ["Laptop-Corporate-01"]
    avg_daily_logins: float = 4.0
    avg_download_mb: float = 45.0
    download_history_json: list[float] = [40.0, 42.0, 45.0, 48.0, 44.0, 46.0, 43.0]

class UserEntityCreate(UserEntityBase):
    id: str

class UserEntityResponse(UserEntityBase):
    id: str
    model_config = ConfigDict(from_attributes=True)
""")

write_file("apps/api/schemas/backup.py", """from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class BackupInventoryBase(BaseModel):
    asset_id: str
    asset_name: str
    backup_type: str = "Incremental"
    backup_status: str = "HEALTHY"
    verified: bool = True
    retention_days: int = 30
    rto_target_hours: float = 4.0
    rto_actual_hours: float = 3.2
    rpo_target_hours: float = 4.0
    rpo_actual_hours: float = 2.5
    test_result: str = "SUCCESS"

class BackupInventoryCreate(BackupInventoryBase):
    id: str
    last_backup: Optional[datetime] = None
    last_test_date: Optional[datetime] = None

class BackupInventoryResponse(BackupInventoryBase):
    id: str
    last_backup: datetime
    last_test_date: datetime
    model_config = ConfigDict(from_attributes=True)
""")

write_file("apps/api/schemas/audit.py", """from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Any

class AuditLogBase(BaseModel):
    actor: str
    role: str = "Analyst"
    action: str
    resource: str
    before_state: Optional[dict[str, Any]] = None
    after_state: Optional[dict[str, Any]] = None
    reason: str

class AuditLogCreate(AuditLogBase):
    id: Optional[str] = None
    timestamp: Optional[datetime] = None

class AuditLogResponse(AuditLogBase):
    id: str
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
""")

write_file("apps/api/schemas/setting.py", """from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class SettingBase(BaseModel):
    key: str
    value: str
    description: Optional[str] = None

class SettingCreate(SettingBase):
    pass

class SettingUpdate(BaseModel):
    value: str
    description: Optional[str] = None

class SettingResponse(SettingBase):
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
""")

print("Fixes applied successfully!")
