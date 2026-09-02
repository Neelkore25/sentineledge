from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from apps.api.core.database import get_db
from apps.api.models.incident import Incident
from apps.api.models.event import SecurityEvent
from apps.api.models.asset import Asset
from apps.api.models.user import UserEntity
from apps.api.services.ai_investigator import AIInvestigatorService

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/investigate")
async def investigate(payload: dict = Body(...), db: Session = Depends(get_db)):
    incident_id = payload.get("incident_id")
    if not incident_id:
        raise HTTPException(status_code=400, detail="incident_id required")

    inc = db.query(Incident).filter(Incident.id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")

    event_ids = inc.event_ids or []
    events = db.query(SecurityEvent).filter(SecurityEvent.id.in_(event_ids)).all() if event_ids else []
    
    asset_entity = db.query(Asset).filter(Asset.asset_name == inc.affected_asset).first()
    user_entity = db.query(UserEntity).filter(UserEntity.username == inc.affected_user).first()

    evidence_package = {
        "incident": {
            "id": inc.id,
            "title": inc.title,
            "affected_user": inc.affected_user,
            "affected_asset": inc.affected_asset,
            "risk_score": inc.risk_score
        },
        "events": [
            {
                "id": e.id,
                "event_type": e.event_type,
                "source_ip": e.source_ip,
                "user_id": e.user_id,
                "endpoint": e.endpoint,
                "bytes_transferred": e.bytes_transferred
            } for e in events
        ],
        "user_baseline": {
            "typical_locations": user_entity.typical_locations if user_entity else ["Mumbai"],
            "download_history_json": user_entity.download_history_json if user_entity else [45.0],
            "typical_login_start_hour": user_entity.typical_login_start_hour if user_entity else 9,
            "typical_login_end_hour": user_entity.typical_login_end_hour if user_entity else 18
        },
        "asset": {
            "asset_name": inc.affected_asset,
            "criticality": asset_entity.criticality if asset_entity else "Tier 2",
            "business_function": asset_entity.business_function if asset_entity else "Enterprise Portal"
        },
        "risk_breakdown": inc.risk_breakdown or {},
        "recovery_context": {"rpo_gap_hours": 0.0}
    }

    result = await AIInvestigatorService.investigate_incident(evidence_package)
    
    inc.ai_summary = result.get("summary")
    inc.ai_hypothesis = result.get("primary_hypothesis")
    inc.ai_alternative = result.get("alternative_explanation")
    inc.ai_missing_evidence = result.get("missing_evidence")
    if result.get("recommended_actions"):
        inc.recommended_action = result["recommended_actions"][0]
    db.commit()

    return result
