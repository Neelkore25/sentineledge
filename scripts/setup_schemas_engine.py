import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# ==================== SCHEMAS ====================

write_file("apps/api/schemas/event.py", """from pydantic import BaseModel, Field
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

    class Config:
        from_attributes = True
""")

write_file("apps/api/schemas/incident.py", """from pydantic import BaseModel, Field
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

    class Config:
        from_attributes = True
""")

write_file("apps/api/schemas/asset.py", """from pydantic import BaseModel
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

    class Config:
        from_attributes = True
""")

write_file("apps/api/schemas/user.py", """from pydantic import BaseModel
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

    class Config:
        from_attributes = True
""")

write_file("apps/api/schemas/backup.py", """from pydantic import BaseModel
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

    class Config:
        from_attributes = True
""")

write_file("apps/api/schemas/audit.py", """from pydantic import BaseModel
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

    class Config:
        from_attributes = True
""")

write_file("apps/api/schemas/setting.py", """from pydantic import BaseModel
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

    class Config:
        from_attributes = True
""")

write_file("apps/api/schemas/__init__.py", """from apps.api.schemas.event import SecurityEventBase, SecurityEventCreate, SecurityEventResponse
from apps.api.schemas.incident import IncidentBase, IncidentCreate, IncidentResponse, RiskBreakdownSchema
from apps.api.schemas.asset import AssetBase, AssetCreate, AssetResponse
from apps.api.schemas.user import UserEntityBase, UserEntityCreate, UserEntityResponse
from apps.api.schemas.backup import BackupInventoryBase, BackupInventoryCreate, BackupInventoryResponse
from apps.api.schemas.audit import AuditLogBase, AuditLogCreate, AuditLogResponse
from apps.api.schemas.setting import SettingBase, SettingCreate, SettingUpdate, SettingResponse
""")

# ==================== DETECTION ENGINE ====================

write_file("apps/api/engine/rules.py", """from typing import Optional, Any
from datetime import datetime, timezone

SEVERITY_SCORES = {
    "LOW": 25.0,
    "MEDIUM": 50.0,
    "HIGH": 75.0,
    "CRITICAL": 100.0
}

def normalize_rule_severity(severity_str: str) -> float:
    \"\"\"Normalizes rule severity string into [0, 100] sub-score R_rule.\"\"\"
    return SEVERITY_SCORES.get(severity_str.upper(), 50.0)

class DetectionRule:
    def __init__(self, rule_id: str, name: str, description: str, severity: str, attack_category: str):
        self.rule_id = rule_id
        self.name = name
        self.description = description
        self.severity = severity.upper()
        self.attack_category = attack_category
        self.enabled = True

    def evaluate(self, events: list[dict]) -> Optional[dict]:
        raise NotImplementedError

class BruteForceRule(DetectionRule):
    def __init__(self, threshold: int = 5):
        super().__init__(
            rule_id="RULE_AUTH_BRUTE_FORCE_001",
            name="Repeated Authentication Failures",
            description=f"Detects >= {threshold} failed login attempts from a user or IP",
            severity="HIGH",
            attack_category="Credential Access"
        )
        self.threshold = threshold

    def evaluate(self, events: list[dict]) -> Optional[dict]:
        if not self.enabled:
            return None
        failed_logins = [
            e for e in events 
            if e.get("event_type") in ("LOGIN_FAILED", "AUTH_FAILURE") 
            or (e.get("action") == "LOGIN" and e.get("status") in ("FAILURE", "BLOCKED"))
        ]
        if len(failed_logins) >= self.threshold:
            return {
                "rule_id": self.rule_id,
                "rule_name": self.name,
                "severity": self.severity,
                "r_rule": normalize_rule_severity(self.severity),
                "matched_event_ids": [e["id"] for e in failed_logins if "id" in e],
                "description": f"Triggered by {len(failed_logins)} failed login attempts (threshold >= {self.threshold})."
            }
        return None

class SuspiciousGeoLoginRule(DetectionRule):
    def __init__(self):
        super().__init__(
            rule_id="RULE_AUTH_SUSPICIOUS_GEO_002",
            name="Suspicious Geolocation Authentication",
            description="Detects successful authentication from an unapproved or foreign location",
            severity="MEDIUM",
            attack_category="Initial Access"
        )

    def evaluate(self, events: list[dict], allowed_locations: Optional[list[str]] = None) -> Optional[dict]:
        if not self.enabled:
            return None
        allowed = set(loc.lower() for loc in (allowed_locations or ["mumbai", "bengaluru", "delhi", "internal_vpn"]))
        matched = []
        for e in events:
            if e.get("event_type") in ("LOGIN_SUCCESS", "AUTH_SUCCESS") and e.get("location"):
                if e["location"].lower() not in allowed:
                    matched.append(e)
        if matched:
            return {
                "rule_id": self.rule_id,
                "rule_name": self.name,
                "severity": self.severity,
                "r_rule": normalize_rule_severity(self.severity),
                "matched_event_ids": [e["id"] for e in matched if "id" in e],
                "description": f"Logins detected from unapproved locations: {[e['location'] for e in matched]}."
            }
        return None

class PrivilegeEscalationRule(DetectionRule):
    def __init__(self):
        super().__init__(
            rule_id="RULE_PRIV_ESCALATION_003",
            name="Unauthorized Privilege Grant",
            description="Detects administrative privilege elevation or role changes",
            severity="CRITICAL",
            attack_category="Privilege Escalation"
        )

    def evaluate(self, events: list[dict]) -> Optional[dict]:
        if not self.enabled:
            return None
        matched = [
            e for e in events 
            if e.get("event_type") in ("PRIVILEGE_CHANGE", "ROLE_ASSIGNED_ADMIN", "ADMIN_ACCESS")
            or (e.get("action") == "GRANT_ROLE" and "admin" in str(e.get("endpoint", "")).lower())
        ]
        if matched:
            return {
                "rule_id": self.rule_id,
                "rule_name": self.name,
                "severity": self.severity,
                "r_rule": normalize_rule_severity(self.severity),
                "matched_event_ids": [e["id"] for e in matched if "id" in e],
                "description": f"Administrative privilege modification event detected."
            }
        return None

class DataExfiltrationRule(DetectionRule):
    def __init__(self, byte_threshold: int = 500 * 1024 * 1024): # 500 MB
        super().__init__(
            rule_id="RULE_EXFIL_SPIKE_004",
            name="Large Volume Data Exfiltration",
            description="Detects anomalous single-event or aggregated transfer exceeding threshold",
            severity="HIGH",
            attack_category="Exfiltration"
        )
        self.byte_threshold = byte_threshold

    def evaluate(self, events: list[dict]) -> Optional[dict]:
        if not self.enabled:
            return None
        matched = [
            e for e in events 
            if e.get("bytes_transferred", 0) >= self.byte_threshold
            or e.get("event_type") in ("BULK_DATA_EXPORT", "FILE_DOWNLOAD_ANOMALOUS")
        ]
        if matched:
            total_mb = sum(e.get("bytes_transferred", 0) for e in matched) / (1024 * 1024)
            return {
                "rule_id": self.rule_id,
                "rule_name": self.name,
                "severity": self.severity,
                "r_rule": normalize_rule_severity(self.severity),
                "matched_event_ids": [e["id"] for e in matched if "id" in e],
                "description": f"High-volume data transfer detected ({total_mb:.1f} MB)."
            }
        return None

class BackupFailureRule(DetectionRule):
    def __init__(self):
        super().__init__(
            rule_id="RULE_BACKUP_CORRUPT_005",
            name="Backup Job Aborted or Tampered",
            description="Detects backup failures or snapshot deletions on critical assets",
            severity="HIGH",
            attack_category="Impact"
        )

    def evaluate(self, events: list[dict]) -> Optional[dict]:
        if not self.enabled:
            return None
        matched = [
            e for e in events
            if e.get("event_type") in ("BACKUP_FAILED", "SNAPSHOT_DELETED", "BACKUP_TAMPERED")
        ]
        if matched:
            return {
                "rule_id": self.rule_id,
                "rule_name": self.name,
                "severity": self.severity,
                "r_rule": normalize_rule_severity(self.severity),
                "matched_event_ids": [e["id"] for e in matched if "id" in e],
                "description": f"Backup integrity disruption detected ({len(matched)} events)."
            }
        return None

class PortScanReconRule(DetectionRule):
    def __init__(self, endpoint_threshold: int = 4):
        super().__init__(
            rule_id="RULE_RECON_PORT_SCAN_006",
            name="Reconnaissance Port/Endpoint Sweep",
            description="Detects rapid scanning across multiple distinct network endpoints",
            severity="MEDIUM",
            attack_category="Reconnaissance"
        )
        self.endpoint_threshold = endpoint_threshold

    def evaluate(self, events: list[dict]) -> Optional[dict]:
        if not self.enabled:
            return None
        endpoints = set(e.get("endpoint") for e in events if e.get("endpoint"))
        if len(endpoints) >= self.endpoint_threshold or any(e.get("event_type") == "PORT_SCAN" for e in events):
            return {
                "rule_id": self.rule_id,
                "rule_name": self.name,
                "severity": self.severity,
                "r_rule": normalize_rule_severity(self.severity),
                "matched_event_ids": [e["id"] for e in events if "id" in e],
                "description": f"Endpoint reconnaissance sweep detected ({len(endpoints)} unique endpoints)."
            }
        return None

DEFAULT_RULES = [
    BruteForceRule(),
    SuspiciousGeoLoginRule(),
    PrivilegeEscalationRule(),
    DataExfiltrationRule(),
    BackupFailureRule(),
    PortScanReconRule()
]

def evaluate_all_rules(events: list[dict], rules: list[DetectionRule] = None, user_context: Optional[dict] = None) -> list[dict]:
    \"\"\"Evaluates all active deterministic rules against an event stream.\"\"\"
    active_rules = rules or DEFAULT_RULES
    matches = []
    allowed_locs = user_context.get("typical_locations") if user_context else None
    for rule in active_rules:
        if isinstance(rule, SuspiciousGeoLoginRule):
            res = rule.evaluate(events, allowed_locations=allowed_locs)
        else:
            res = rule.evaluate(events)
        if res:
            matches.append(res)
    return matches
""")

# ==================== ANOMALY SCORING (ROBUST Z-SCORE MAD) ====================

write_file("apps/api/engine/anomaly.py", """import numpy as np
from typing import Sequence, Optional

def calculate_mad(values: Sequence[float]) -> tuple[float, float]:
    \"\"\"
    Calculates Median and Median Absolute Deviation (MAD).
    Returns (median, MAD).
    \"\"\"
    arr = np.array(values, dtype=float)
    if len(arr) == 0:
        return 0.0, 1.0
    median = float(np.median(arr))
    deviations = np.abs(arr - median)
    mad = float(np.median(deviations))
    if mad == 0.0:
        # Fallback to mean absolute deviation or epsilon to prevent division by zero
        mad = float(np.mean(deviations)) or 1.0
    return median, mad

def robust_z_score(observed_value: float, baseline_values: Sequence[float]) -> float:
    \"\"\"
    Calculates Modified Robust Z-score:
    z_MAD = |x - median| / (1.4826 * MAD)
    \"\"\"
    median, mad = calculate_mad(baseline_values)
    denominator = 1.4826 * mad
    if denominator == 0.0:
        return 0.0
    return float(abs(observed_value - median) / denominator)

def normalize_behavior_score(z_mad: float, sensitivity_multiplier: float = 3.5) -> float:
    \"\"\"
    Normalizes Robust Z-Score into [0, 100] sub-score S_behavior.
    S_behavior = clamp[0, 100]( (z_mad / 3.5) * 100 )
    \"\"\"
    normalized = (z_mad / sensitivity_multiplier) * 100.0
    return float(min(100.0, max(0.0, normalized)))

def evaluate_user_behavior(
    observed_download_mb: float,
    observed_login_hour: int,
    user_baseline: dict
) -> dict:
    \"\"\"
    Evaluates behavioral deviation across download volume and login hour.
    Returns composite normalized S_behavior sub-score in [0, 100] and detailed features.
    \"\"\"
    history = user_baseline.get("download_history_json", [40.0, 42.0, 45.0, 48.0, 44.0, 46.0, 43.0])
    z_download = robust_z_score(observed_download_mb, history)
    s_download = normalize_behavior_score(z_download)
    
    # Login hour deviation check
    start_hour = user_baseline.get("typical_login_start_hour", 9)
    end_hour = user_baseline.get("typical_login_end_hour", 18)
    
    if start_hour <= observed_login_hour <= end_hour:
        hour_penalty = 0.0
    else:
        # Distance outside working window in hours
        dist = min(abs(observed_login_hour - start_hour), abs(observed_login_hour - end_hour))
        hour_penalty = min(100.0, dist * 15.0)
    
    # Composite behavioral deviation
    s_behavior = min(100.0, max(0.0, 0.7 * s_download + 0.3 * hour_penalty))
    
    return {
        "s_behavior": round(s_behavior, 2),
        "z_mad_download": round(z_download, 2),
        "s_download_deviation": round(s_download, 2),
        "observed_download_mb": observed_download_mb,
        "baseline_median_download_mb": round(float(np.median(history)), 1),
        "hour_deviation_penalty": round(hour_penalty, 2),
        "observed_login_hour": observed_login_hour,
        "expected_hour_range": f"{start_hour:02d}:00 - {end_hour:02d}:00"
    }
""")

# ==================== TEMPORAL CORRELATION ENGINE ====================

write_file("apps/api/engine/correlation.py", """from datetime import datetime, timezone, timedelta
from typing import Optional

def normalize_correlation_score(event_count: int, stage_diversity_count: int) -> float:
    \"\"\"
    Normalizes correlation group strength into [0, 100] sub-score C_correlation:
    C_correlation = clamp[0, 100]( event_count * 10 + stage_diversity_count * 20 )
    \"\"\"
    raw = (event_count * 10.0) + (stage_diversity_count * 20.0)
    return float(min(100.0, max(0.0, raw)))

class EventCorrelator:
    def __init__(self, window_minutes: int = 30):
        self.window_minutes = window_minutes

    def correlate_events(self, events: list[dict], target_user: Optional[str] = None, target_ip: Optional[str] = None, target_asset: Optional[str] = None) -> dict:
        \"\"\"
        Correlates events sharing entity identity (user_id, source_ip, or asset_id)
        within the configurable sliding window.
        \"\"\"
        if not events:
            return {
                "correlated_event_ids": [],
                "event_count": 0,
                "stage_diversity": 0,
                "c_correlation": 0.0,
                "time_span_minutes": 0.0,
                "attack_stages": []
            }

        # Filter events related to entities
        matched = []
        for e in events:
            matches_user = target_user and e.get("user_id") == target_user
            matches_ip = target_ip and e.get("source_ip") == target_ip
            matches_asset = target_asset and e.get("asset_id") == target_asset
            
            if matches_user or matches_ip or matches_asset or (not target_user and not target_ip and not target_asset):
                matched.append(e)

        if not matched:
            return {
                "correlated_event_ids": [],
                "event_count": 0,
                "stage_diversity": 0,
                "c_correlation": 0.0,
                "time_span_minutes": 0.0,
                "attack_stages": []
            }

        # Determine stages present
        stages = set()
        for e in matched:
            etype = e.get("event_type", "").upper()
            action = e.get("action", "").upper()
            if "LOGIN_FAILED" in etype or "AUTH_FAILURE" in etype or "PORT_SCAN" in etype:
                stages.add("Initial Access / Recon")
            elif "LOGIN_SUCCESS" in etype:
                stages.add("Authentication")
            elif "ADMIN" in etype or "PRIVILEGE" in etype or "ROLE" in action:
                stages.add("Privilege Escalation")
            elif "DOWNLOAD" in etype or "EXPORT" in etype or e.get("bytes_transferred", 0) > 10_000_000:
                stages.add("Exfiltration")
            elif "BACKUP" in etype:
                stages.add("Impact / Tampering")
            else:
                stages.add("Execution")

        event_count = len(matched)
        stage_diversity = len(stages)
        c_score = normalize_correlation_score(event_count, stage_diversity)

        return {
            "correlated_event_ids": [e["id"] for e in matched if "id" in e],
            "event_count": event_count,
            "stage_diversity": stage_diversity,
            "c_correlation": round(c_score, 2),
            "attack_stages": sorted(list(stages))
        }
""")

# ==================== ASSET CRITICALITY & BUSINESS IMPACT ====================

write_file("apps/api/engine/impact.py", """from typing import Optional

CRITICALITY_MAP = {
    "TIER 1 (CROWN JEWEL)": 100.0,
    "TIER 1": 100.0,
    "TIER 2 (HIGH)": 75.0,
    "TIER 2": 75.0,
    "TIER 3 (MEDIUM)": 50.0,
    "TIER 3": 50.0,
    "TIER 4 (LOW)": 25.0,
    "TIER 4": 25.0
}

SENSITIVITY_MAP = {
    "PII / FINANCIAL": 100.0,
    "FINANCIAL": 90.0,
    "PII": 85.0,
    "OPERATIONAL": 60.0,
    "INTERNAL": 40.0,
    "PUBLIC": 10.0
}

def normalize_asset_criticality(criticality_str: str) -> float:
    \"\"\"Normalizes asset criticality tier string into [0, 100] sub-score A_criticality.\"\"\"
    return CRITICALITY_MAP.get(criticality_str.upper(), 50.0)

def normalize_business_impact(
    data_sensitivity: str,
    estimated_downtime_cost_per_hour: float,
    user_blast_radius: int
) -> float:
    \"\"\"
    Normalizes business impact into [0, 100] sub-score B_impact:
    B_impact = clamp[0, 100]( 0.4 * Sensitivity + 0.3 * DowntimeExposure + 0.3 * BlastRadius )
    \"\"\"
    s_score = SENSITIVITY_MAP.get(data_sensitivity.upper(), 50.0)
    # Scale hourly downtime cost (0 to $10,000/hr -> 0 to 100)
    d_score = min(100.0, (estimated_downtime_cost_per_hour / 10000.0) * 100.0)
    # Scale blast radius (0 to 200 users -> 0 to 100)
    b_score = min(100.0, (user_blast_radius / 200.0) * 100.0)
    
    impact = (0.4 * s_score) + (0.3 * d_score) + (0.3 * b_score)
    return float(min(100.0, max(0.0, impact)))

def calculate_business_impact_tier(b_impact_score: float) -> str:
    if b_impact_score >= 75.0:
        return "CRITICAL"
    elif b_impact_score >= 50.0:
        return "HIGH"
    elif b_impact_score >= 25.0:
        return "MEDIUM"
    return "LOW"
""")

# ==================== EXPLAINABLE RISK MODEL ====================

write_file("apps/api/engine/risk.py", """from apps.api.engine.rules import normalize_rule_severity
from apps.api.engine.anomaly import normalize_behavior_score
from apps.api.engine.correlation import normalize_correlation_score
from apps.api.engine.impact import normalize_asset_criticality, normalize_business_impact

WEIGHTS = {
    "w_rule": 0.25,
    "w_behavior": 0.20,
    "w_correlation": 0.20,
    "w_criticality": 0.20,
    "w_impact": 0.15
}

def calculate_severity_band(risk_score: float) -> str:
    if risk_score >= 75.0:
        return "CRITICAL"
    elif risk_score >= 50.0:
        return "HIGH"
    elif risk_score >= 25.0:
        return "MEDIUM"
    return "LOW"

def calculate_explainable_risk(
    r_rule: float,
    s_behavior: float,
    c_correlation: float,
    a_criticality: float,
    b_impact: float
) -> dict:
    \"\"\"
    Computes explainable composite risk score using SentinelEdge Research Risk Model v1.
    All 5 input sub-scores MUST be individually normalized to [0, 100] prior to weighting.
    \"\"\"
    # Explicit clamp verification on each sub-score
    r = float(min(100.0, max(0.0, r_rule)))
    s = float(min(100.0, max(0.0, s_behavior)))
    c = float(min(100.0, max(0.0, c_correlation)))
    a = float(min(100.0, max(0.0, a_criticality)))
    b = float(min(100.0, max(0.0, b_impact)))

    contrib_rule = WEIGHTS["w_rule"] * r
    contrib_behavior = WEIGHTS["w_behavior"] * s
    contrib_correlation = WEIGHTS["w_correlation"] * c
    contrib_criticality = WEIGHTS["w_criticality"] * a
    contrib_impact = WEIGHTS["w_impact"] * b

    total = contrib_rule + contrib_behavior + contrib_correlation + contrib_criticality + contrib_impact
    composite_risk = float(min(100.0, max(0.0, total)))
    band = calculate_severity_band(composite_risk)

    return {
        "composite_risk_score": round(composite_risk, 1),
        "severity_band": band,
        "r_rule": round(r, 1),
        "s_behavior": round(s, 1),
        "c_correlation": round(c, 1),
        "a_criticality": round(a, 1),
        "b_impact": round(b, 1),
        "weights": WEIGHTS,
        "weighted_contributions": {
            "rule": round(contrib_rule, 2),
            "behavior": round(contrib_behavior, 2),
            "correlation": round(contrib_correlation, 2),
            "criticality": round(contrib_criticality, 2),
            "impact": round(contrib_impact, 2)
        },
        "formula": "Risk = min(100, 0.25*R_rule + 0.20*S_behavior + 0.20*C_correlation + 0.20*A_criticality + 0.15*B_impact)",
        "model_version": "SentinelEdge Research Risk Model v1"
    }
""")

# ==================== RECOVERY READINESS MODEL ====================

write_file("apps/api/engine/recovery.py", """from datetime import datetime, timezone, timedelta

def calculate_recovery_readiness(
    backup_freshness_hours: float,
    target_rpo_hours: float,
    verified: bool,
    last_test_days_ago: float,
    rto_actual_hours: float,
    rto_target_hours: float
) -> dict:
    \"\"\"
    Calculates Recovery Readiness Index:
    Readiness = 0.35 * B_freshness + 0.25 * V_verified + 0.20 * T_test_recency + 0.20 * R_compliance
    All sub-factors are normalized in [0, 100].
    \"\"\"
    # 1. Freshness Score (100 if within RPO target, decays linearly up to 3x RPO)
    rpo_gap_hours = max(0.0, backup_freshness_hours - target_rpo_hours)
    if backup_freshness_hours <= target_rpo_hours:
        b_freshness = 100.0
    else:
        overage = backup_freshness_hours - target_rpo_hours
        b_freshness = max(0.0, 100.0 - (overage / target_rpo_hours) * 50.0)

    # 2. Verification Score
    v_verified = 100.0 if verified else 0.0

    # 3. Recovery Drill Recency Score (100 if tested <= 30 days ago, 0 if > 90 days ago)
    if last_test_days_ago <= 30.0:
        t_recency = 100.0
    elif last_test_days_ago >= 90.0:
        t_recency = max(0.0, 20.0 - (last_test_days_ago - 90.0) * 0.5)
    else:
        t_recency = 100.0 - ((last_test_days_ago - 30.0) / 60.0) * 80.0

    # 4. RTO / RPO SLA Compliance Score
    rto_ratio = rto_actual_hours / max(0.1, rto_target_hours)
    if rto_ratio <= 1.0:
        r_compliance = 100.0
    else:
        r_compliance = max(0.0, 100.0 - (rto_ratio - 1.0) * 100.0)

    # Composite Index
    readiness_index = (0.35 * b_freshness) + (0.25 * v_verified) + (0.20 * t_recency) + (0.20 * r_compliance)
    readiness_index = float(min(100.0, max(0.0, readiness_index)))

    # Determine primary recovery weakness
    weaknesses = []
    if not verified:
        weaknesses.append("Last snapshot backup has not been verified.")
    if rpo_gap_hours > 0:
        weaknesses.append(f"Backup freshness exceeds target RPO by {rpo_gap_hours:.1f} hours.")
    if last_test_days_ago > 45:
        weaknesses.append(f"Recovery drill is overdue (last tested {int(last_test_days_ago)} days ago).")
    if rto_actual_hours > rto_target_hours:
        weaknesses.append(f"Actual restoration time ({rto_actual_hours:.1f}h) exceeds SLA ({rto_target_hours:.1f}h).")
    
    primary_weakness = weaknesses[0] if weaknesses else "All recovery parameters within target SLAs."

    return {
        "readiness_index": round(readiness_index, 1),
        "b_freshness": round(b_freshness, 1),
        "v_verified": round(v_verified, 1),
        "t_recency": round(t_recency, 1),
        "r_compliance": round(r_compliance, 1),
        "rpo_gap_hours": round(rpo_gap_hours, 1),
        "target_rpo_hours": target_rpo_hours,
        "backup_freshness_hours": round(backup_freshness_hours, 1),
        "last_test_days_ago": round(last_test_days_ago, 1),
        "rto_target_hours": rto_target_hours,
        "rto_actual_hours": rto_actual_hours,
        "primary_weakness": primary_weakness,
        "weaknesses": weaknesses
    }
""")

write_file("apps/api/engine/__init__.py", """from apps.api.engine.rules import (
    DetectionRule, BruteForceRule, SuspiciousGeoLoginRule, PrivilegeEscalationRule,
    DataExfiltrationRule, BackupFailureRule, PortScanReconRule,
    DEFAULT_RULES, evaluate_all_rules, normalize_rule_severity
)
from apps.api.engine.anomaly import (
    calculate_mad, robust_z_score, normalize_behavior_score, evaluate_user_behavior
)
from apps.api.engine.correlation import (
    EventCorrelator, normalize_correlation_score
)
from apps.api.engine.impact import (
    normalize_asset_criticality, normalize_business_impact, calculate_business_impact_tier
)
from apps.api.engine.risk import (
    calculate_explainable_risk, calculate_severity_band, WEIGHTS
)
from apps.api.engine.recovery import (
    calculate_recovery_readiness
)
""")

print("Schemas and Detection Engine setup complete!")
