from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from apps.api.core.database import get_db
from apps.api.models.setting import SystemSetting

router = APIRouter(prefix="/settings", tags=["settings"])

@router.get("")
def get_settings(db: Session = Depends(get_db)):
    records = db.query(SystemSetting).all()
    return {
        r.key: {
            "value": r.value,
            "description": r.description,
            "updated_at": r.updated_at.isoformat()
        } for r in records
    }

@router.put("/{key}")
def update_setting(key: str, payload: dict = Body(...), db: Session = Depends(get_db)):
    if "value" not in payload:
        raise HTTPException(status_code=400, detail="'value' field required in payload.")
    
    rec = db.query(SystemSetting).filter(SystemSetting.key == key).first()
    if not rec:
        rec = SystemSetting(
            key=key,
            value=str(payload["value"]),
            description=payload.get("description", "Dynamic configuration setting"),
            updated_at=datetime.now(timezone.utc)
        )
        db.add(rec)
    else:
        rec.value = str(payload["value"])
        if "description" in payload:
            rec.description = payload["description"]
        rec.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(rec)
    return {
        "key": rec.key,
        "value": rec.value,
        "description": rec.description,
        "updated_at": rec.updated_at.isoformat()
    }
