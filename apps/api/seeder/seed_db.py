from datetime import datetime, timezone, timedelta
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
