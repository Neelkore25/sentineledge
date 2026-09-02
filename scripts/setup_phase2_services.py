import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# 1. Scenarios and Synthetic Seeder
write_file("apps/api/seeder/scenarios.py", """from datetime import datetime, timezone, timedelta

SCENARIO_TEMPLATES = {
    "brute_force": {
        "id": "scenario_brute_force",
        "name": "Too Many Doors",
        "category": "Credential Access",
        "description": "Rapid succession of 15 failed authentication attempts against the Admin Auth Portal followed by a suspicious login.",
        "target_asset_id": "ASSET_AUTH_PORTAL",
        "target_user_id": "usr_finance_admin",
        "source_ip": "194.26.29.114",
        "location": "Bucharest, RO",
        "events": [
            {
                "event_type": "LOGIN_FAILED",
                "action": "LOGIN",
                "status": "FAILURE",
                "endpoint": "/api/v1/auth/login",
                "source": "auth_service",
                "device_id": "Unknown-Device-Linux",
                "bytes_transferred": 512,
                "event_metadata": {"reason": "Invalid password", "attempt_index": i}
            } for i in range(1, 13)
        ] + [
            {
                "event_type": "LOGIN_SUCCESS",
                "action": "LOGIN",
                "status": "SUCCESS",
                "endpoint": "/api/v1/auth/login",
                "source": "auth_service",
                "device_id": "Unknown-Device-Linux",
                "bytes_transferred": 2048,
                "event_metadata": {"mfa_prompted": False, "session_created": True}
            },
            {
                "event_type": "ADMIN_ACCESS",
                "action": "LIST_ACCOUNTS",
                "status": "SUCCESS",
                "endpoint": "/api/v1/admin/users",
                "source": "auth_service",
                "device_id": "Unknown-Device-Linux",
                "bytes_transferred": 14200,
                "event_metadata": {"query": "SELECT * FROM users"}
            }
        ]
    },
    "suspicious_login": {
        "id": "scenario_suspicious_login",
        "name": "Unexpected Visitor",
        "category": "Initial Access",
        "description": "Off-hours login (03:15 AM) from a new foreign IP address and unmanaged device bypassing standard geofencing.",
        "target_asset_id": "ASSET_ERP_PORTAL",
        "target_user_id": "usr_ops_lead",
        "source_ip": "185.220.101.5",
        "location": "Frankfurt, DE",
        "events": [
            {
                "event_type": "LOGIN_SUCCESS",
                "action": "LOGIN",
                "status": "SUCCESS",
                "endpoint": "/portal/sso",
                "source": "vpn_gateway",
                "device_id": "Win10-Unmanaged-BYOD",
                "bytes_transferred": 4096,
                "event_metadata": {"country": "DE", "is_tor_exit_node": True}
            },
            {
                "event_type": "FILE_DOWNLOAD",
                "action": "DOWNLOAD",
                "status": "SUCCESS",
                "endpoint": "/portal/invoices/q3_summary.pdf",
                "source": "erp_portal",
                "device_id": "Win10-Unmanaged-BYOD",
                "bytes_transferred": 15_000_000,
                "event_metadata": {"filename": "q3_summary.pdf"}
            }
        ]
    },
    "privilege_jump": {
        "id": "scenario_privilege_jump",
        "name": "The Privilege Jump",
        "category": "Privilege Escalation",
        "description": "Standard engineering account abruptly assigned Super-Admin permissions without an associated change ticket.",
        "target_asset_id": "ASSET_ACTIVE_DIR",
        "target_user_id": "usr_dev_intern",
        "source_ip": "10.0.4.55",
        "location": "Mumbai, IN",
        "events": [
            {
                "event_type": "API_REQUEST",
                "action": "QUERY_ROLES",
                "status": "SUCCESS",
                "endpoint": "/api/v1/iam/roles",
                "source": "iam_service",
                "device_id": "Laptop-Corporate-DEV09",
                "bytes_transferred": 8192,
                "event_metadata": {"role_queried": "DomainAdmin"}
            },
            {
                "event_type": "PRIVILEGE_CHANGE",
                "action": "GRANT_ROLE",
                "status": "SUCCESS",
                "endpoint": "/api/v1/iam/assign",
                "source": "iam_service",
                "device_id": "Laptop-Corporate-DEV09",
                "bytes_transferred": 1024,
                "event_metadata": {"granted_role": "SuperAdministrator", "ticket_id": None}
            }
        ]
    },
    "data_exfiltration": {
        "id": "scenario_data_exfiltration",
        "name": "The Large Download",
        "category": "Exfiltration",
        "description": "High-volume compressed SQL database dump transfer (2.8 GB) initiated during non-working hours.",
        "target_asset_id": "ASSET_CUSTOMER_DB",
        "target_user_id": "usr_finance_admin",
        "source_ip": "10.0.2.14",
        "location": "Mumbai, IN",
        "events": [
            {
                "event_type": "DB_QUERY",
                "action": "EXECUTE_EXPORT",
                "status": "SUCCESS",
                "endpoint": "/db/export/customers_full.sql.gz",
                "source": "database_server",
                "device_id": "Laptop-Corporate-FIN01",
                "bytes_transferred": 50_000,
                "event_metadata": {"table": "customers_financial_pii", "rows": 450000}
            },
            {
                "event_type": "FILE_DOWNLOAD",
                "action": "EGRESS_TRANSFER",
                "status": "SUCCESS",
                "endpoint": "/external/cloud_upload",
                "source": "network_egress",
                "device_id": "Laptop-Corporate-FIN01",
                "bytes_transferred": 2_800_000_000,
                "event_metadata": {"destination": "https://transfer.sh/drop", "duration_sec": 140}
            }
        ]
    },
    "multi_stage": {
        "id": "scenario_multi_stage",
        "name": "The Long Night",
        "category": "Multi-Stage Compromise",
        "description": "Full-spectrum kill chain: Reconnaissance sweep -> Brute force -> Privilege grant -> Bulk exfiltration.",
        "target_asset_id": "ASSET_CUSTOMER_DB",
        "target_user_id": "usr_finance_admin",
        "source_ip": "194.26.29.200",
        "location": "Bucharest, RO",
        "events": [
            {
                "event_type": "PORT_SCAN",
                "action": "PROBE",
                "status": "BLOCKED",
                "endpoint": "/port/8080",
                "source": "edge_firewall",
                "device_id": "Scanner-Node",
                "bytes_transferred": 256,
                "event_metadata": {"ports": [22, 80, 443, 3306, 5432, 8080]}
            },
            {
                "event_type": "LOGIN_FAILED",
                "action": "LOGIN",
                "status": "FAILURE",
                "endpoint": "/api/v1/auth/login",
                "source": "auth_service",
                "device_id": "Scanner-Node",
                "bytes_transferred": 512,
                "event_metadata": {"attempt": 1}
            },
            {
                "event_type": "LOGIN_FAILED",
                "action": "LOGIN",
                "status": "FAILURE",
                "endpoint": "/api/v1/auth/login",
                "source": "auth_service",
                "device_id": "Scanner-Node",
                "bytes_transferred": 512,
                "event_metadata": {"attempt": 2}
            },
            {
                "event_type": "LOGIN_FAILED",
                "action": "LOGIN",
                "status": "FAILURE",
                "endpoint": "/api/v1/auth/login",
                "source": "auth_service",
                "device_id": "Scanner-Node",
                "bytes_transferred": 512,
                "event_metadata": {"attempt": 3}
            },
            {
                "event_type": "LOGIN_SUCCESS",
                "action": "LOGIN",
                "status": "SUCCESS",
                "endpoint": "/api/v1/auth/login",
                "source": "auth_service",
                "device_id": "Scanner-Node",
                "bytes_transferred": 2048,
                "event_metadata": {"compromised_credential": True}
            },
            {
                "event_type": "PRIVILEGE_CHANGE",
                "action": "GRANT_ROLE",
                "status": "SUCCESS",
                "endpoint": "/api/v1/iam/assign",
                "source": "iam_service",
                "device_id": "Scanner-Node",
                "bytes_transferred": 1024,
                "event_metadata": {"granted": "FullAdmin"}
            },
            {
                "event_type": "FILE_DOWNLOAD",
                "action": "EGRESS_TRANSFER",
                "status": "SUCCESS",
                "endpoint": "/external/cloud_upload",
                "source": "network_egress",
                "device_id": "Scanner-Node",
                "bytes_transferred": 1_900_000_000,
                "event_metadata": {"file": "production_backup.tar.gz"}
            }
        ]
    },
    "recon_sweep": {
        "id": "scenario_recon_sweep",
        "name": "Recon in the Dark",
        "category": "Reconnaissance",
        "description": "Broad port and service enumeration probing edge endpoints from an external scanner.",
        "target_asset_id": "ASSET_AUTH_PORTAL",
        "target_user_id": None,
        "source_ip": "45.154.255.88",
        "location": "Sofia, BG",
        "events": [
            {
                "event_type": "PORT_SCAN",
                "action": "SYN_SCAN",
                "status": "BLOCKED",
                "endpoint": f"/probe/port_{p}",
                "source": "edge_firewall",
                "device_id": "Unknown-Scanner",
                "bytes_transferred": 128,
                "event_metadata": {"port": p}
            } for p in [21, 22, 23, 25, 80, 443, 1433, 3306, 3389, 5432, 6379, 8080, 9200]
        ]
    },
    "backup_failure": {
        "id": "scenario_backup_failure",
        "name": "Backup Severed",
        "category": "Impact",
        "description": "Automated snapshot job failed and backup integrity check flagged corrupted replica on the primary DB.",
        "target_asset_id": "ASSET_CUSTOMER_DB",
        "target_user_id": "usr_backup_svc",
        "source_ip": "10.0.1.99",
        "location": "Mumbai, IN",
        "events": [
            {
                "event_type": "BACKUP_FAILED",
                "action": "SNAPSHOT_CREATE",
                "status": "FAILURE",
                "endpoint": "/backup/v2/snapshot",
                "source": "backup_daemon",
                "device_id": "Backup-Server-01",
                "bytes_transferred": 0,
                "event_metadata": {"error": "Volume lock timeout", "asset": "Customer Financial DB"}
            },
            {
                "event_type": "BACKUP_TAMPERED",
                "action": "VERIFY_REPLICA",
                "status": "FAILURE",
                "endpoint": "/backup/v2/verify",
                "source": "backup_daemon",
                "device_id": "Backup-Server-01",
                "bytes_transferred": 4096,
                "event_metadata": {"checksum_mismatch": True}
            }
        ]
    }
}
""")

# 2. Database Seeder
write_file("apps/api/seeder/seed_db.py", """from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from apps.api.models.asset import Asset
from apps.api.models.user import UserEntity
from apps.api.models.backup import BackupInventory
from apps.api.models.setting import SystemSetting
from apps.api.models.event import SecurityEvent
from apps.api.models.incident import Incident
from apps.api.models.audit import AuditLog
from apps.api.engine.risk import calculate_explainable_risk

def seed_database(db: Session):
    # Check if already seeded
    if db.query(Asset).first():
        return

    now = datetime.now(timezone.utc)

    # 1. Assets
    assets = [
        Asset(
            id="ASSET_CUSTOMER_DB",
            asset_name="Customer Financial Database",
            asset_type="PostgreSQL RDS",
            criticality="Tier 1 (Crown Jewel)",
            owner="Data Engineering / CISO",
            business_function="Customer Payment & Transaction Processing",
            data_sensitivity="PII / Financial",
            estimated_downtime_cost_per_hour=8500.0,
            user_blast_radius=180
        ),
        Asset(
            id="ASSET_AUTH_PORTAL",
            asset_name="Admin Identity & Auth Gateway",
            asset_type="OAuth2 / Keycloak",
            criticality="Tier 1 (Crown Jewel)",
            owner="SecOps Infrastructure",
            business_function="Organization-wide Single Sign-On",
            data_sensitivity="Operational",
            estimated_downtime_cost_per_hour=6000.0,
            user_blast_radius=200
        ),
        Asset(
            id="ASSET_ERP_PORTAL",
            asset_name="Enterprise ERP Suite",
            asset_type="Web Application",
            criticality="Tier 2 (High)",
            owner="Operations & Finance",
            business_function="Supply Chain, Invoicing & Payroll",
            data_sensitivity="Financial",
            estimated_downtime_cost_per_hour=3500.0,
            user_blast_radius=95
        ),
        Asset(
            id="ASSET_ACTIVE_DIR",
            asset_name="Internal IAM / Directory Service",
            asset_type="Active Directory LDAP",
            criticality="Tier 2 (High)",
            owner="IT Helpdesk",
            business_function="Employee Access & Device Management",
            data_sensitivity="Internal",
            estimated_downtime_cost_per_hour=2500.0,
            user_blast_radius=150
        ),
        Asset(
            id="ASSET_INTERNAL_WIKI",
            asset_name="Engineering Knowledge Base",
            asset_type="Notion / Confluence",
            criticality="Tier 3 (Medium)",
            owner="Engineering Lead",
            business_function="Internal Documentation & Runbooks",
            data_sensitivity="Internal",
            estimated_downtime_cost_per_hour=450.0,
            user_blast_radius=40
        )
    ]
    for a in assets:
        db.add(a)

    # 2. Users
    users = [
        UserEntity(
            id="usr_finance_admin",
            username="finance_admin",
            full_name="Priya Sharma",
            role="Finance Lead / Admin",
            typical_login_start_hour=9,
            typical_login_end_hour=18,
            typical_locations=["Mumbai", "Bengaluru"],
            typical_devices=["Laptop-Corporate-FIN01"],
            avg_daily_logins=4.0,
            avg_download_mb=45.0,
            download_history_json=[38.0, 42.0, 45.0, 50.0, 44.0, 47.0, 41.0]
        ),
        UserEntity(
            id="usr_ops_lead",
            username="ops_lead",
            full_name="Rohan Varma",
            role="Operations Manager",
            typical_login_start_hour=8,
            typical_login_end_hour=19,
            typical_locations=["Bengaluru", "Mumbai"],
            typical_devices=["MacBook-Ops-02"],
            avg_daily_logins=6.0,
            avg_download_mb=120.0,
            download_history_json=[110.0, 115.0, 125.0, 130.0, 118.0, 122.0]
        ),
        UserEntity(
            id="usr_dev_intern",
            username="dev_intern",
            full_name="Aarav Mehta",
            role="Junior Software Engineer",
            typical_login_start_hour=10,
            typical_login_end_hour=19,
            typical_locations=["Pune", "Mumbai"],
            typical_devices=["Laptop-Corporate-DEV09"],
            avg_daily_logins=3.0,
            avg_download_mb=80.0,
            download_history_json=[70.0, 75.0, 85.0, 90.0, 80.0, 78.0]
        )
    ]
    for u in users:
        db.add(u)

    # 3. Backups
    backups = [
        BackupInventory(
            id="BK-01",
            asset_id="ASSET_CUSTOMER_DB",
            asset_name="Customer Financial Database",
            last_backup=now - timedelta(hours=3),
            backup_type="Immutable Snapshot",
            backup_status="HEALTHY",
            verified=True,
            retention_days=90,
            rto_target_hours=2.0,
            rto_actual_hours=1.8,
            rpo_target_hours=4.0,
            rpo_actual_hours=3.0,
            last_test_date=now - timedelta(days=12),
            test_result="SUCCESS"
        ),
        BackupInventory(
            id="BK-02",
            asset_id="ASSET_AUTH_PORTAL",
            asset_name="Admin Identity & Auth Gateway",
            last_backup=now - timedelta(hours=6),
            backup_type="Differential",
            backup_status="HEALTHY",
            verified=True,
            retention_days=30,
            rto_target_hours=4.0,
            rto_actual_hours=3.2,
            rpo_target_hours=6.0,
            rpo_actual_hours=6.0,
            last_test_date=now - timedelta(days=28),
            test_result="SUCCESS"
        ),
        BackupInventory(
            id="BK-03",
            asset_id="ASSET_ERP_PORTAL",
            asset_name="Enterprise ERP Suite",
            last_backup=now - timedelta(hours=18),
            backup_type="Incremental",
            backup_status="DEGRADED",
            verified=False,
            retention_days=30,
            rto_target_hours=4.0,
            rto_actual_hours=5.5,
            rpo_target_hours=4.0,
            rpo_actual_hours=18.0,
            last_test_date=now - timedelta(days=64),
            test_result="PARTIAL"
        )
    ]
    for b in backups:
        db.add(b)

    # 4. System Settings
    settings_records = [
        SystemSetting(
            key="correlation_window_minutes",
            value="30",
            description="Temporal correlation sliding window for grouping related security events (minutes)."
        ),
        SystemSetting(
            key="brute_force_threshold",
            value="5",
            description="Minimum failed authentication attempts before triggering RULE_AUTH_BRUTE_FORCE_001."
        ),
        SystemSetting(
            key="data_exfil_threshold_mb",
            value="500",
            description="Byte threshold in MB for triggering RULE_EXFIL_SPIKE_004."
        ),
        SystemSetting(
            key="ai_provider",
            value="local",
            description="Selected AI investigation provider (local | openai | gemini | anthropic)."
        )
    ]
    for s in settings_records:
        db.add(s)

    # 5. Initial Seed Incident
    risk_info = calculate_explainable_risk(
        r_rule=75.0,
        s_behavior=68.0,
        c_correlation=80.0,
        a_criticality=100.0,
        b_impact=88.0
    )

    seed_incident = Incident(
        id="INC-1042",
        title="Correlated Credential Compromise & Recon Sweep",
        description="Automated multi-layer detection flagged 12 failed authentication attempts followed by a successful login from Romanian IP 194.26.29.114 on Admin Auth Gateway.",
        severity="CRITICAL",
        risk_score=risk_info["composite_risk_score"],
        status="OPEN",
        detected_at=now - timedelta(minutes=45),
        first_seen=now - timedelta(minutes=50),
        last_seen=now - timedelta(minutes=45),
        affected_asset="Admin Identity & Auth Gateway",
        affected_user="finance_admin",
        attack_category="Credential Access",
        business_impact="CRITICAL",
        confidence=0.91,
        correlation_group="CORR-AUTH-194.26.29.114",
        event_ids=["EV-SEED-01", "EV-SEED-02", "EV-SEED-03", "EV-SEED-04", "EV-SEED-05"],
        risk_breakdown=risk_info,
        ai_summary="Observed rapid failed authentication bursts targeting finance_admin followed immediately by successful admin session instantiation from an anomalous Romanian IP range.",
        ai_hypothesis="Probable distributed credential stuffing or password spray attack achieving valid initial session authentication.",
        ai_alternative="Legitimate executive remote login through unapproved VPN or foreign travel roaming.",
        ai_missing_evidence="Host-level endpoint process logs confirming whether local credential dumping occurred.",
        recommended_action="Simulate temporary session revocation and mandate Out-of-Band MFA re-verification for user finance_admin."
    )
    db.add(seed_incident)

    # 6. Seed Events
    seed_events = [
        SecurityEvent(
            id=f"EV-SEED-0{i}",
            timestamp=now - timedelta(minutes=50 - i),
            source="auth_service",
            user_id="finance_admin",
            asset_id="ASSET_AUTH_PORTAL",
            source_ip="194.26.29.114",
            event_type="LOGIN_FAILED" if i < 5 else "LOGIN_SUCCESS",
            action="LOGIN",
            status="FAILURE" if i < 5 else "SUCCESS",
            endpoint="/api/v1/auth/login",
            device_id="Unknown-Linux-Node",
            location="Bucharest, RO",
            bytes_transferred=1024 * i,
            event_metadata={"seed": True, "attempt": i}
        ) for i in range(1, 6)
    ]
    for e in seed_events:
        db.add(e)

    # 7. Initial Audit Log
    db.add(AuditLog(
        id="AUD-INIT-01",
        timestamp=now - timedelta(minutes=40),
        actor="SentinelEdge Detection Engine",
        role="System",
        action="INCIDENT_CORRELATED_AUTO",
        resource="Incident #INC-1042",
        before_state={"status": "NO_INCIDENT"},
        after_state={"status": "OPEN", "risk_score": risk_info["composite_risk_score"]},
        reason="Automated detection engine correlated 5 events into Incident INC-1042."
    ))

    db.commit()
    print("Database seeded with realistic baseline assets, users, backups, settings, events, and seed incident.")
""")

# 3. AI Investigator Service
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
        if any("LOGIN_FAILED" in et for et in event_types):
            failed_evs = [e["id"] for e in events if "LOGIN_FAILED" in e.get("event_type", "")]
            evidence_citations.append(f"Repeated authentication failures observed across event IDs: {', '.join(failed_evs[:4])}.")
        if any("LOGIN_SUCCESS" in et for et in event_types):
            succ_evs = [e["id"] for e in events if "LOGIN_SUCCESS" in e.get("event_type", "")]
            evidence_citations.append(f"Successful session authentication established in event ID: {', '.join(succ_evs)}.")
        if any("PRIVILEGE" in et or "ADMIN" in et for et in event_types):
            priv_evs = [e["id"] for e in events if "PRIVILEGE" in e.get("event_type", "") or "ADMIN" in e.get("event_type", "")]
            evidence_citations.append(f"Privilege modification or administrative elevation detected in: {', '.join(priv_evs)}.")
        if any("DOWNLOAD" in et or e.get("bytes_transferred", 0) > 50_000_000 for e in events for et in [e.get("event_type", "")]):
            exfil_evs = [e["id"] for e in events if e.get("bytes_transferred", 0) > 50_000_000 or "DOWNLOAD" in e.get("event_type", "")]
            evidence_citations.append(f"Anomalous high-volume outbound data transfer detected in: {', '.join(exfil_evs)}.")

        if not evidence_citations:
            evidence_citations = [f"Correlated {len(events)} telemetry events referencing IDs: {', '.join(event_ids[:5])}."]

        # Formulate grounded hypothesis
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
        # If API key configured and provider is not local, attempt external provider
        provider = settings.AI_PROVIDER.lower()
        api_key = settings.AI_API_KEY

        if provider in ("openai", "gemini", "anthropic") and api_key:
            try:
                # Structured system prompt enforcing strict evidence contract
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
                        resp = await client.post(
                            "https://api.openai.com/v1/chat/completions",
                            headers={"Authorization": f"Bearer {api_key}"},
                            json={
                                "model": settings.AI_MODEL or "gpt-4o-mini",
                                "messages": [
                                    {"role": "system", "content": system_prompt},
                                    {"role": "user", "content": f"Investigate this evidence package and return JSON with summary, primary_hypothesis, alternative_explanation, evidence_citations (list), missing_evidence, confidence_score (float 0-1), recommended_actions (list):\n{user_content}"}
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

        # Fallback to deterministic local engine
        return cls.generate_deterministic_analysis(evidence_package)
""")

print("Phase 2 seeder, scenarios, and AI investigator service created!")
