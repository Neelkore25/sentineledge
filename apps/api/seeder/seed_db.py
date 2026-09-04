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
    """
    Initializes foundational baseline infrastructure records (Assets, User Baselines,
    Backup SLA Targets, and System Settings).
    
    IMPORTANT: Normal production startup starts CLEAN without auto-inserting
    fake breaches or incidents.
    """
    # Check if foundational assets are already initialized
    if db.query(Asset).first():
        return

    now = datetime.now(timezone.utc)

    # 1. Critical Infrastructure Assets (Required for Criticality Scoring)
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

    # 2. User Baseline Profiles (Required for MAD Anomaly Detection)
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

    # 3. Backup SLA Configurations (Required for Recovery Posture Index)
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
            description="Sliding window duration for grouping related events into incidents (minutes)."
        ),
        SystemSetting(
            key="brute_force_threshold",
            value="5",
            description="Minimum failed login attempts before triggering brute-force detection rule."
        ),
        SystemSetting(
            key="data_exfil_threshold_mb",
            value="500",
            description="Byte threshold in MB for flagging anomalous large data export spikes."
        ),
        SystemSetting(
            key="ai_provider",
            value="local",
            description="AI investigation provider (local deterministic | openai | gemini)."
        )
    ]
    for s in settings_records:
        db.add(s)

    db.commit()
    print("Initialized foundational assets, user baselines, and backup configurations (Clean state).")

def reset_to_clean_state(db: Session):
    """Purges all security events, incidents, and non-system audit records."""
    db.query(Incident).delete()
    db.query(SecurityEvent).delete()
    db.query(AuditLog).delete()
    
    # Add clean reset audit record
    now = datetime.now(timezone.utc)
    db.add(AuditLog(
        id="AUD-RESET-01",
        timestamp=now,
        actor="Security Administrator",
        role="Admin",
        action="DATABASE_RESET",
        resource="System Database",
        reason="System reset to clean empty state (all events and incidents purged)."
    ))
    db.commit()
    return {"status": "clean", "message": "Database reset to clean state."}

def seed_demo_scenario(db: Session):
    """Explicit opt-in helper to populate a synthetic breach incident for demonstration."""
    now = datetime.now(timezone.utc)
    risk_info = calculate_explainable_risk(
        r_rule=85.0,
        s_behavior=78.0,
        c_correlation=80.0,
        a_criticality=100.0,
        b_impact=88.0
    )

    demo_inc = Incident(
        id="INC-DEMO-101",
        title="[DEMO] Correlated Credential Compromise & Exfil Spike",
        description="[SYNTHETIC DEMO DATA] Automated 3-layer detection flagged authentication burst from Romanian IP 194.26.29.114 followed by off-hours data exfiltration.",
        severity="CRITICAL",
        risk_score=risk_info["composite_risk_score"],
        status="OPEN",
        detected_at=now - timedelta(minutes=15),
        first_seen=now - timedelta(minutes=25),
        last_seen=now - timedelta(minutes=15),
        affected_asset="Customer Financial Database",
        affected_user="sarah_connor",
        attack_category="Credential Access & Exfiltration",
        business_impact="CRITICAL",
        confidence=0.92,
        correlation_group="CORR-DEMO-194.26.29.114",
        event_ids=["EV-DEMO-01", "EV-DEMO-02", "EV-DEMO-03"],
        risk_breakdown=risk_info,
        ai_summary="Observed rapid authentication failures followed by admin login and 2.8 GB outbound egress transfer to external IP.",
        ai_hypothesis="Probable stolen session credential followed by unauthorized customer database dump.",
        ai_alternative="Authorized remote disaster recovery export by senior DBA.",
        ai_missing_evidence="Database query logs confirming exact tables accessed during session.",
        recommended_action="Revoke active user session and mandate immediate password reset.",
        created_at=now - timedelta(minutes=15),
        updated_at=now - timedelta(minutes=15)
    )
    db.add(demo_inc)

    events = [
        SecurityEvent(
            id="EV-DEMO-01",
            timestamp=now - timedelta(minutes=25),
            source="auth_gateway",
            user_id="sarah_connor",
            asset_id="ASSET_AUTH_PORTAL",
            source_ip="194.26.29.114",
            event_type="LOGIN_FAILED",
            action="LOGIN",
            status="FAILURE",
            endpoint="/api/v1/auth/login",
            location="Bucharest, RO",
            bytes_transferred=1024,
            event_metadata={"demo": True, "attempt": 1}
        ),
        SecurityEvent(
            id="EV-DEMO-02",
            timestamp=now - timedelta(minutes=20),
            source="auth_gateway",
            user_id="sarah_connor",
            asset_id="ASSET_AUTH_PORTAL",
            source_ip="194.26.29.114",
            event_type="LOGIN_SUCCESS",
            action="LOGIN",
            status="SUCCESS",
            endpoint="/api/v1/auth/login",
            location="Bucharest, RO",
            bytes_transferred=2048,
            event_metadata={"demo": True, "mfa": False}
        ),
        SecurityEvent(
            id="EV-DEMO-03",
            timestamp=now - timedelta(minutes=15),
            source="database_proxy",
            user_id="sarah_connor",
            asset_id="ASSET_CUSTOMER_DB",
            source_ip="194.26.29.114",
            event_type="DATA_EGRESS",
            action="SQL_DUMP",
            status="SUCCESS",
            endpoint="/api/v1/data/export",
            location="Bucharest, RO",
            bytes_transferred=2800000000,
            event_metadata={"demo": True, "query": "SELECT * FROM customer_financial_records", "rows": 450000}
        )
    ]
    for e in events:
        db.add(e)

    db.add(AuditLog(
        id="AUD-DEMO-01",
        timestamp=now - timedelta(minutes=15),
        actor="SentinelEdge Simulation Engine",
        role="System",
        action="DEMO_SCENARIO_LOADED",
        resource="Incident/INC-DEMO-101",
        reason="User explicitly requested demo breach scenario loading."
    ))
    db.commit()
    return {"status": "success", "incident_id": "INC-DEMO-101"}
