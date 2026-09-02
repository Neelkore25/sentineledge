from fastapi import APIRouter, Depends, Query, HTTPException
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
