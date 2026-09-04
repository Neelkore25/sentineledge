from typing import Optional, Any
from datetime import datetime, timezone

SEVERITY_SCORES = {
    "LOW": 25.0,
    "MEDIUM": 50.0,
    "HIGH": 75.0,
    "CRITICAL": 100.0
}

def normalize_rule_severity(severity_str: str) -> float:
    """Normalizes rule severity string into [0, 100] sub-score R_rule."""
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
            if str(e.get("event_type", "")).upper() in ("LOGIN_FAILED", "AUTH_FAILURE") 
            or (str(e.get("event_type", "")).lower() in ("login_attempt", "login", "auth") and str(e.get("status", "")).upper() in ("FAILURE", "FAILED", "BLOCKED"))
            or (str(e.get("action", "")).upper() in ("LOGIN", "LOGIN_ATTEMPT") and str(e.get("status", "")).upper() in ("FAILURE", "FAILED", "BLOCKED"))
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
            ev_type = str(e.get("event_type", "")).upper()
            if ev_type in ("LOGIN_SUCCESS", "AUTH_SUCCESS") and e.get("location"):
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
            if str(e.get("event_type", "")).upper() in ("PRIVILEGE_CHANGE", "ROLE_ASSIGNED_ADMIN", "ADMIN_ACCESS")
            or (str(e.get("action", "")).upper() == "GRANT_ROLE" and "admin" in str(e.get("endpoint", "")).lower())
            or str(e.get("event_metadata", {}).get("anomaly_type", "")).lower() == "off_hours_privileged_access"
            or str(e.get("anomaly_type", "")).lower() == "off_hours_privileged_access"
            or e.get("is_anomaly") == 1
            or e.get("event_metadata", {}).get("is_anomaly") == 1
        ]
        if matched:
            return {
                "rule_id": self.rule_id,
                "rule_name": self.name,
                "severity": self.severity,
                "r_rule": normalize_rule_severity(self.severity),
                "matched_event_ids": [e["id"] for e in matched if "id" in e],
                "description": f"Administrative privilege modification event detected ({len(matched)} matches)."
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
    """Evaluates all active deterministic rules against an event stream."""
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
