from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.api.core.database import get_db
from apps.api.models.audit import AuditLog

router = APIRouter(prefix="/audit", tags=["audit"])

@router.get("")
def get_audit_logs(limit: int = 50, db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()
    return [
        {
            "id": l.id,
            "timestamp": l.timestamp.isoformat(),
            "actor": l.actor,
            "role": l.role,
            "action": l.action,
            "resource": l.resource,
            "before_state": l.before_state,
            "after_state": l.after_state,
            "reason": l.reason
        } for l in logs
    ]
