from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
import uuid
from apps.api.core.database import get_db
from apps.api.models.event import SecurityEvent
from apps.api.models.incident import Incident
from apps.api.models.asset import Asset
from apps.api.models.user import UserEntity
from apps.api.models.setting import SystemSetting
from apps.api.models.audit import AuditLog
from apps.api.seeder.scenarios import SCENARIO_TEMPLATES
from apps.api.seeder.seed_db import reset_to_clean_state, seed_demo_scenario
from apps.api.engine.rules import evaluate_all_rules, DEFAULT_RULES
from apps.api.engine.anomaly import evaluate_user_behavior
from apps.api.engine.correlation import EventCorrelator
from apps.api.engine.impact import normalize_asset_criticality, normalize_business_impact, calculate_business_impact_tier
from apps.api.engine.risk import calculate_explainable_risk
from apps.api.services.ai_investigator import AIInvestigatorService

router = APIRouter(prefix="/simulation", tags=["simulation"])

@router.get("/scenarios")
def get_scenarios():
    return [
        {
            "id": s["id"],
            "key": key,
            "name": s["name"],
            "category": s["category"],
            "description": s["description"],
            "event_count": len(s["events"]),
            "target_asset": s["target_asset_id"],
            "target_user": s["target_user_id"]
        } for key, s in SCENARIO_TEMPLATES.items()
    ]

@router.post("/reset")
def reset_database(db: Session = Depends(get_db)):
    """Resets the database to a clean 0-breach state (purges all events, incidents, and audit logs)."""
    return reset_to_clean_state(db)

@router.post("/seed-demo")
def seed_demo(db: Session = Depends(get_db)):
    """Explicitly seeds a synthetic breach scenario for testing and demonstration."""
    return seed_demo_scenario(db)

@router.post("/run")
async def run_scenario(payload: dict = Body(...), db: Session = Depends(get_db)):
    scenario_key = payload.get("scenario_key", "brute_force")
    if scenario_key not in SCENARIO_TEMPLATES:
        raise HTTPException(status_code=400, detail=f"Scenario '{scenario_key}' not found.")

    scenario = SCENARIO_TEMPLATES[scenario_key]
    now = datetime.now(timezone.utc)

    # 1. Ingest scenario events into DB
    created_events = []
    for i, item in enumerate(scenario["events"]):
        ev_id = f"EV-SIM-{uuid.uuid4().hex[:6].upper()}"
        ts = now - timedelta(seconds=(len(scenario["events"]) - i) * 8)
        ev = SecurityEvent(
            id=ev_id,
            timestamp=ts,
            source=item.get("source", "sim_generator"),
            user_id=scenario.get("target_user_id"),
            asset_id=scenario.get("target_asset_id"),
            source_ip=scenario.get("source_ip", "194.26.29.114"),
            event_type=item.get("event_type"),
            action=item.get("action"),
            status=item.get("status"),
            endpoint=item.get("endpoint"),
            device_id=item.get("device_id"),
            location=scenario.get("location", "Bucharest, RO"),
            bytes_transferred=item.get("bytes_transferred", 0),
            event_metadata=item.get("event_metadata", {})
        )
        db.add(ev)
        created_events.append(ev)
    db.commit()

    # 2. Query dynamic settings for correlation window
    setting_record = db.query(SystemSetting).filter(SystemSetting.key == "correlation_window_minutes").first()
    corr_window = int(setting_record.value) if setting_record else 30

    # 3. Run Detection Engine Layer 1 (Rules)
    event_dicts = [
        {
            "id": e.id,
            "event_type": e.event_type,
            "action": e.action,
            "status": e.status,
            "endpoint": e.endpoint,
            "location": e.location,
            "bytes_transferred": e.bytes_transferred,
            "source_ip": e.source_ip,
            "user_id": e.user_id,
            "asset_id": e.asset_id
        } for e in created_events
    ]
    
    user_entity = db.query(UserEntity).filter(UserEntity.id == scenario.get("target_user_id")).first() if scenario.get("target_user_id") else None
    user_context = {
        "typical_locations": user_entity.typical_locations if user_entity else ["Mumbai", "Bengaluru"],
        "download_history_json": user_entity.download_history_json if user_entity else [40.0, 42.0, 45.0],
        "typical_login_start_hour": user_entity.typical_login_start_hour if user_entity else 9,
        "typical_login_end_hour": user_entity.typical_login_end_hour if user_entity else 18
    }

    rule_matches = evaluate_all_rules(event_dicts, user_context=user_context)
    r_rule = max([m["r_rule"] for m in rule_matches]) if rule_matches else 35.0

    # 4. Run Detection Engine Layer 2 (MAD Behavioral Anomaly)
    max_bytes = max([e.bytes_transferred for e in created_events], default=0)
    observed_download_mb = max_bytes / (1024 * 1024)
    observed_hour = now.hour
    behavior_res = evaluate_user_behavior(observed_download_mb, observed_hour, user_context)
    s_behavior = behavior_res["s_behavior"]

    # 5. Run Detection Engine Layer 3 (Temporal Correlation)
    correlator = EventCorrelator(window_minutes=corr_window)
    corr_res = correlator.correlate_events(
        event_dicts,
        target_user=scenario.get("target_user_id"),
        target_ip=scenario.get("source_ip"),
        target_asset=scenario.get("target_asset_id")
    )
    c_correlation = corr_res["c_correlation"]

    # 6. Query Asset Criticality & Business Impact
    asset_entity = db.query(Asset).filter(Asset.id == scenario.get("target_asset_id")).first()
    if asset_entity:
        a_criticality = normalize_asset_criticality(asset_entity.criticality)
        b_impact = normalize_business_impact(
            asset_entity.data_sensitivity,
            asset_entity.estimated_downtime_cost_per_hour,
            asset_entity.user_blast_radius
        )
        asset_name = asset_entity.asset_name
    else:
        a_criticality = 75.0
        b_impact = 70.0
        asset_name = "Corporate Service"

    b_impact_tier = calculate_business_impact_tier(b_impact)

    # 7. Compute Explainable Risk Score
    risk_breakdown = calculate_explainable_risk(
        r_rule=r_rule,
        s_behavior=s_behavior,
        c_correlation=c_correlation,
        a_criticality=a_criticality,
        b_impact=b_impact
    )

    # 8. Create Correlated Incident
    inc_id = f"INC-{uuid.uuid4().hex[:6].upper()}"
    incident_title = f"{scenario['name']} - {scenario['category']} on {asset_name}"
    incident_desc = f"Simulated detection generated {len(created_events)} events. Rule matches: {[m['rule_name'] for m in rule_matches]}. Behavioral deviation: {s_behavior}%. Correlation group strength: {c_correlation}%."

    evidence_package = {
        "incident": {
            "id": inc_id,
            "title": incident_title,
            "affected_user": scenario.get("target_user_id"),
            "affected_asset": asset_name,
            "risk_score": risk_breakdown["composite_risk_score"]
        },
        "events": event_dicts,
        "user_baseline": user_context,
        "asset": {
            "asset_name": asset_name,
            "criticality": asset_entity.criticality if asset_entity else "Tier 2",
            "business_function": asset_entity.business_function if asset_entity else "Enterprise Operations"
        },
        "risk_breakdown": risk_breakdown,
        "recovery_context": {"rpo_gap_hours": 0.0}
    }

    ai_analysis = await AIInvestigatorService.investigate_incident(evidence_package)

    now_utc = datetime.now(timezone.utc)
    new_incident = Incident(
        id=inc_id,
        title=incident_title,
        description=incident_desc,
        severity=risk_breakdown["severity_band"],
        risk_score=risk_breakdown["composite_risk_score"],
        status="OPEN",
        detected_at=now_utc,
        first_seen=created_events[0].timestamp,
        last_seen=created_events[-1].timestamp,
        affected_asset=asset_name,
        affected_user=scenario.get("target_user_id"),
        attack_category=scenario["category"],
        business_impact=b_impact_tier,
        confidence=0.92,
        correlation_group=f"CORR-{scenario_key.upper()}-{scenario.get('source_ip', 'LOCAL')}",
        event_ids=[e.id for e in created_events],
        risk_breakdown=risk_breakdown,
        ai_summary=ai_analysis.get("summary"),
        ai_hypothesis=ai_analysis.get("primary_hypothesis"),
        ai_alternative=ai_analysis.get("alternative_explanation"),
        ai_missing_evidence=ai_analysis.get("missing_evidence"),
        recommended_action=ai_analysis.get("recommended_actions", ["Acknowledge incident and review telemetry."])[0],
        created_at=now_utc,
        updated_at=now_utc
    )
    db.add(new_incident)

    # 9. Audit log entry
    db.add(AuditLog(
        id=f"AUD-{uuid.uuid4().hex[:8].upper()}",
        timestamp=now_utc,
        actor="Simulation Engine",
        role="System",
        action="SCENARIO_EXECUTED",
        resource=f"Scenario: {scenario['name']} -> Incident #{inc_id}",
        before_state={"scenario": scenario_key},
        after_state={"incident_id": inc_id, "risk_score": risk_breakdown["composite_risk_score"], "event_count": len(created_events)},
        reason=f"User ran simulation scenario '{scenario['name']}' in Simulation Lab."
    ))

    db.commit()

    return {
        "status": "completed",
        "scenario_name": scenario["name"],
        "incident_id": inc_id,
        "risk_score": risk_breakdown["composite_risk_score"],
        "severity": risk_breakdown["severity_band"],
        "events_generated": len(created_events),
        "rule_matches": [m["rule_name"] for m in rule_matches],
        "risk_breakdown": risk_breakdown,
        "ai_investigation": ai_analysis
    }
