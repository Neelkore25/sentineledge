import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# 1. Telemetry Router
write_file("apps/api/routers/telemetry.py", """from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timezone
import uuid
from apps.api.core.database import get_db
from apps.api.models.event import SecurityEvent
from apps.api.schemas.event import SecurityEventResponse, SecurityEventCreate

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
""")

# 2. Incidents Router
write_file("apps/api/routers/incidents.py", """from fastapi import APIRouter, Depends, Query, HTTPException, Body
from sqlalchemy.orm import Session
from typing import Optional, Any
from datetime import datetime, timezone
import uuid
from apps.api.core.database import get_db
from apps.api.models.incident import Incident
from apps.api.models.audit import AuditLog
from apps.api.models.event import SecurityEvent

router = APIRouter(prefix="/incidents", tags=["incidents"])

@router.get("")
def list_incidents(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    attack_category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Incident)
    if status and status.upper() != "ALL":
        query = query.filter(Incident.status == status.upper())
    if severity and severity.upper() != "ALL":
        query = query.filter(Incident.severity == severity.upper())
    if attack_category and attack_category.upper() != "ALL":
        query = query.filter(Incident.attack_category.ilike(f"%{attack_category}%"))
    if search:
        query = query.filter(
            (Incident.title.ilike(f"%{search}%")) |
            (Incident.affected_asset.ilike(f"%{search}%")) |
            (Incident.affected_user.ilike(f"%{search}%")) |
            (Incident.id.ilike(f"%{search}%"))
        )

    incidents = query.order_by(Incident.detected_at.desc()).all()
    return [
        {
            "id": inc.id,
            "title": inc.title,
            "description": inc.description,
            "severity": inc.severity,
            "risk_score": inc.risk_score,
            "status": inc.status,
            "detected_at": inc.detected_at.isoformat(),
            "first_seen": inc.first_seen.isoformat(),
            "last_seen": inc.last_seen.isoformat(),
            "affected_asset": inc.affected_asset,
            "affected_user": inc.affected_user,
            "attack_category": inc.attack_category,
            "business_impact": inc.business_impact,
            "confidence": inc.confidence,
            "correlation_group": inc.correlation_group,
            "event_ids": inc.event_ids or [],
            "risk_breakdown": inc.risk_breakdown or {},
            "ai_summary": inc.ai_summary,
            "ai_hypothesis": inc.ai_hypothesis,
            "ai_alternative": inc.ai_alternative,
            "ai_missing_evidence": inc.ai_missing_evidence,
            "recommended_action": inc.recommended_action,
            "created_at": inc.created_at.isoformat(),
            "updated_at": inc.updated_at.isoformat()
        } for inc in incidents
    ]

@router.get("/{incident_id}")
def get_incident(incident_id: str, db: Session = Depends(get_db)):
    inc = db.query(Incident).filter(Incident.id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")

    event_ids = inc.event_ids or []
    events = db.query(SecurityEvent).filter(SecurityEvent.id.in_(event_ids)).all() if event_ids else []

    return {
        "incident": {
            "id": inc.id,
            "title": inc.title,
            "description": inc.description,
            "severity": inc.severity,
            "risk_score": inc.risk_score,
            "status": inc.status,
            "detected_at": inc.detected_at.isoformat(),
            "first_seen": inc.first_seen.isoformat(),
            "last_seen": inc.last_seen.isoformat(),
            "affected_asset": inc.affected_asset,
            "affected_user": inc.affected_user,
            "attack_category": inc.attack_category,
            "business_impact": inc.business_impact,
            "confidence": inc.confidence,
            "correlation_group": inc.correlation_group,
            "event_ids": inc.event_ids or [],
            "risk_breakdown": inc.risk_breakdown or {},
            "ai_summary": inc.ai_summary,
            "ai_hypothesis": inc.ai_hypothesis,
            "ai_alternative": inc.ai_alternative,
            "ai_missing_evidence": inc.ai_missing_evidence,
            "recommended_action": inc.recommended_action,
            "created_at": inc.created_at.isoformat(),
            "updated_at": inc.updated_at.isoformat()
        },
        "related_events": [
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

@router.patch("/{incident_id}/status")
def update_incident_status(
    incident_id: str,
    status_update: dict = Body(...),
    db: Session = Depends(get_db)
):
    inc = db.query(Incident).filter(Incident.id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")

    new_status = status_update.get("status", "INVESTIGATING").upper()
    reason = status_update.get("reason", "Status updated by analyst.")
    actor = status_update.get("actor", "Analyst (Demo)")
    role = status_update.get("role", "Analyst")

    old_status = inc.status
    inc.status = new_status
    inc.updated_at = datetime.now(timezone.utc)

    audit = AuditLog(
        id=f"AUD-{uuid.uuid4().hex[:8].upper()}",
        timestamp=datetime.now(timezone.utc),
        actor=actor,
        role=role,
        action="UPDATE_INCIDENT_STATUS",
        resource=f"Incident #{inc.id}",
        before_state={"status": old_status},
        after_state={"status": new_status},
        reason=reason
    )
    db.add(audit)
    db.commit()

    return {"status": "updated", "incident_id": inc.id, "new_status": inc.status}

@router.post("/{incident_id}/respond")
def execute_response_action(
    incident_id: str,
    action_payload: dict = Body(...),
    db: Session = Depends(get_db)
):
    inc = db.query(Incident).filter(Incident.id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")

    action_type = action_payload.get("action_type", "SIMULATE_ACCOUNT_LOCK")
    actor = action_payload.get("actor", "Analyst (Demo)")
    role = action_payload.get("role", "Analyst")
    reason = action_payload.get("reason", "Human-approved remediation action executed.")
    target = action_payload.get("target", inc.affected_user or inc.affected_asset)

    old_status = inc.status
    inc.status = "MITIGATED"
    inc.updated_at = datetime.now(timezone.utc)

    audit = AuditLog(
        id=f"AUD-{uuid.uuid4().hex[:8].upper()}",
        timestamp=datetime.now(timezone.utc),
        actor=actor,
        role=role,
        action=action_type,
        resource=f"Target: {target} | Incident #{inc.id}",
        before_state={"incident_status": old_status, "containment": "UNCONTAINED"},
        after_state={"incident_status": "MITIGATED", "containment": "CONTAINED", "action_applied": action_type},
        reason=reason
    )
    db.add(audit)
    db.commit()

    return {
        "status": "executed",
        "action_type": action_type,
        "incident_id": inc.id,
        "new_status": inc.status,
        "audit_id": audit.id,
        "message": f"Successfully executed response action '{action_type}' for incident {inc.id}."
    }
""")

print("Part 1 routers written.")
