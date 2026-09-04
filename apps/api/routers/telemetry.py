from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timezone
import uuid
from apps.api.core.database import get_db
from apps.api.models.event import SecurityEvent
from apps.api.models.incident import Incident
from apps.api.models.asset import Asset
from apps.api.models.audit import AuditLog
from apps.api.schemas.event import SecurityEventResponse, SecurityEventCreate
from apps.api.engine.rules import evaluate_all_rules
from apps.api.engine.anomaly import evaluate_user_behavior
from apps.api.engine.correlation import EventCorrelator
from apps.api.engine.impact import normalize_asset_criticality, normalize_business_impact, calculate_business_impact_tier
from apps.api.engine.risk import calculate_explainable_risk

router = APIRouter(prefix="/telemetry", tags=["telemetry"])

@router.get("", response_model=dict)
def get_events(
    skip: int = 0,
    limit: int = 50,
    event_type: Optional[str] = None,
    source_ip: Optional[str] = None,
    user_id: Optional[str] = None,
    asset_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(SecurityEvent)
    if event_type:
        query = query.filter(SecurityEvent.event_type == event_type)
    if source_ip:
        query = query.filter(SecurityEvent.source_ip == source_ip)
    if user_id:
        query = query.filter(SecurityEvent.user_id == user_id)
    if asset_id:
        query = query.filter(SecurityEvent.asset_id == asset_id)
    if status:
        query = query.filter(SecurityEvent.status == status)

    total = query.count()
    events = query.order_by(SecurityEvent.timestamp.desc()).offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": [
            {
                "id": e.id,
                "timestamp": e.timestamp.isoformat(),
                "source": e.source,
                "user_id": e.user_id,
                "asset_id": e.asset_id,
                "source_ip": e.source_ip,
                "event_type": e.event_type,
                "action": e.action,
                "status": e.status,
                "endpoint": e.endpoint,
                "device_id": e.device_id,
                "location": e.location,
                "bytes_transferred": e.bytes_transferred,
                "event_metadata": e.event_metadata
            } for e in events
        ]
    }

@router.get("/{event_id}")
def get_event_by_id(event_id: str, db: Session = Depends(get_db)):
    event = db.query(SecurityEvent).filter(SecurityEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found")
    return {
        "id": event.id,
        "timestamp": event.timestamp.isoformat(),
        "source": event.source,
        "user_id": event.user_id,
        "asset_id": event.asset_id,
        "source_ip": event.source_ip,
        "event_type": event.event_type,
        "action": event.action,
        "status": event.status,
        "endpoint": event.endpoint,
        "device_id": event.device_id,
        "location": event.location,
        "bytes_transferred": event.bytes_transferred,
        "event_metadata": event.event_metadata
    }

@router.post("", response_model=dict)
def ingest_event(event_in: SecurityEventCreate, db: Session = Depends(get_db)):
    ev_id = event_in.id or f"EV-{uuid.uuid4().hex[:8].upper()}"
    ts = event_in.timestamp or datetime.now(timezone.utc)
    ev = SecurityEvent(
        id=ev_id,
        timestamp=ts,
        source=event_in.source,
        user_id=event_in.user_id,
        asset_id=event_in.asset_id,
        source_ip=event_in.source_ip,
        event_type=event_in.event_type,
        action=event_in.action,
        status=event_in.status,
        endpoint=event_in.endpoint,
        device_id=event_in.device_id,
        location=event_in.location,
        bytes_transferred=event_in.bytes_transferred,
        event_metadata=event_in.event_metadata
    )
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return {"status": "ingested", "event_id": ev.id}

@router.post("/batch", response_model=dict)
def ingest_batch_events(events_in: List[SecurityEventCreate], db: Session = Depends(get_db)):
    created_events = []
    dict_events = []
    for item in events_in:
        ev_id = item.id or f"EV-{uuid.uuid4().hex[:8].upper()}"
        ts = item.timestamp or datetime.now(timezone.utc)
        ev = SecurityEvent(
            id=ev_id,
            timestamp=ts,
            source=item.source,
            user_id=item.user_id,
            asset_id=item.asset_id,
            source_ip=item.source_ip,
            event_type=item.event_type,
            action=item.action,
            status=item.status,
            endpoint=item.endpoint,
            device_id=item.device_id,
            location=item.location,
            bytes_transferred=item.bytes_transferred,
            event_metadata=item.event_metadata
        )
        db.add(ev)
        created_events.append(ev)
        dict_events.append({
            "id": ev_id,
            "timestamp": ts,
            "source": item.source,
            "user_id": item.user_id,
            "asset_id": item.asset_id,
            "source_ip": item.source_ip,
            "event_type": item.event_type,
            "action": item.action,
            "status": item.status,
            "endpoint": item.endpoint,
            "device_id": item.device_id,
            "location": item.location,
            "bytes_transferred": item.bytes_transferred,
            "event_metadata": item.event_metadata
        })
    
    db.commit()
    
    target_asset = next((e.asset_id for e in created_events if e.asset_id), "ASSET_CUSTOMER_DB")
    target_user = next((e.user_id for e in created_events if e.user_id), "sarah_connor")
    target_ip = next((e.source_ip for e in created_events if e.source_ip), "10.20.0.1")
    
    # 1. Rule evaluation
    rule_results = evaluate_all_rules(dict_events)
    r_rule = max([r["r_rule"] for r in rule_results]) if rule_results else 30.0
    
    # 2. Behavioral evaluation (MAD)
    now_utc = datetime.now(timezone.utc)
    max_bytes = max([e.bytes_transferred for e in created_events], default=0)
    observed_download_mb = max_bytes / (1024 * 1024)
    user_context = {"download_history_json": [40.0, 42.0, 45.0], "typical_login_start_hour": 9, "typical_login_end_hour": 18}
    beh_eval = evaluate_user_behavior(observed_download_mb, now_utc.hour, user_context)
    s_behavior = beh_eval["s_behavior"]
    
    # 3. Correlation
    correlator = EventCorrelator()
    corr_res = correlator.correlate_events(dict_events, target_user=target_user, target_ip=target_ip, target_asset=target_asset)
    c_correlation = corr_res["c_correlation"]
    
    # 4. Criticality & Impact
    asset = db.query(Asset).filter(Asset.id == target_asset).first()
    if asset:
        a_crit = normalize_asset_criticality(asset.criticality)
        b_impact = normalize_business_impact(
            data_sensitivity=asset.data_sensitivity,
            estimated_downtime_cost_per_hour=asset.estimated_downtime_cost_per_hour,
            user_blast_radius=asset.user_blast_radius
        )
        asset_display_name = asset.asset_name
    else:
        a_crit = 75.0
        b_impact = 70.0
        asset_display_name = target_asset
    impact_tier = calculate_business_impact_tier(b_impact)
    
    # 5. Composite Risk
    risk_res = calculate_explainable_risk(
        r_rule=r_rule,
        s_behavior=s_behavior,
        c_correlation=c_correlation,
        a_criticality=a_crit,
        b_impact=b_impact
    )
    
    # Generate Correlated Incident
    inc_id = f"INC-{uuid.uuid4().hex[:6].upper()}"
    first_ts = min(e.timestamp for e in created_events)
    last_ts = max(e.timestamp for e in created_events)
    
    new_inc = Incident(
        id=inc_id,
        title=f"Custom Telemetry Scan ({len(created_events)} events)",
        description=f"Correlated {len(created_events)} custom telemetry events into threat incident.",
        severity=risk_res["severity_band"],
        risk_score=risk_res["composite_risk_score"],
        status="OPEN",
        detected_at=now_utc,
        first_seen=first_ts,
        last_seen=last_ts,
        affected_asset=asset_display_name,
        affected_user=target_user,
        attack_category="Custom Telemetry Analysis",
        business_impact=impact_tier,
        confidence=min(100.0, float(len(created_events) * 20.0)),
        correlation_group=f"GRP-CUSTOM-{uuid.uuid4().hex[:4].upper()}",
        event_ids=[e.id for e in created_events],
        risk_breakdown=risk_res,
        ai_summary="Custom security telemetry scan analyzed by SentinelEdge 3-layer detection engine.",
        recommended_action="Inspect correlated event timeline, review MAD deviations, and confirm backup posture.",
        created_at=now_utc,
        updated_at=now_utc
    )
    db.add(new_inc)
    
    audit = AuditLog(
        id=f"AUD-{uuid.uuid4().hex[:8].upper()}",
        timestamp=now_utc,
        actor="Security Analyst",
        role="SOC Analyst",
        action="INGEST_CUSTOM_BATCH",
        resource=f"Incident/{inc_id}",
        reason=f"Ingested and analyzed {len(created_events)} custom telemetry events via JSON API"
    )
    db.add(audit)
    db.commit()
    
    return {
        "status": "success",
        "events_ingested": len(created_events),
        "incident_id": inc_id,
        "risk_score": risk_res["composite_risk_score"],
        "severity": risk_res["severity_band"],
        "rule_matches": [r["rule_name"] for r in rule_results],
        "s_behavior": s_behavior,
        "c_correlation": c_correlation,
        "target_asset": target_asset
    }
