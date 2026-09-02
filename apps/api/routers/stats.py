from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from apps.api.core.database import get_db
from apps.api.models.incident import Incident
from apps.api.models.event import SecurityEvent
from apps.api.models.backup import BackupInventory
from apps.api.engine.recovery import calculate_recovery_readiness

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/overview")
def get_overview_stats(db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)

    incidents = db.query(Incident).all()
    open_incidents = [i for i in incidents if i.status in ("OPEN", "INVESTIGATING")]
    
    sev_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
    for i in open_incidents:
        s = i.severity.upper() if i.severity else "MEDIUM"
        sev_counts[s] = sev_counts.get(s, 0) + 1

    if open_incidents:
        avg_risk = sum(i.risk_score for i in open_incidents) / len(open_incidents)
    else:
        avg_risk = 18.0

    last_event = db.query(SecurityEvent).order_by(SecurityEvent.timestamp.desc()).first()
    if last_event:
        last_event_dt = last_event.timestamp.replace(tzinfo=timezone.utc) if last_event.timestamp.tzinfo is None else last_event.timestamp
        last_event_sec = int(max(0, (now - last_event_dt).total_seconds()))
    else:
        last_event_sec = 12

    backups = db.query(BackupInventory).all()
    total_r = 0.0
    for b in backups:
        last_bk_dt = b.last_backup.replace(tzinfo=timezone.utc) if b.last_backup.tzinfo is None else b.last_backup
        last_test_dt = b.last_test_date.replace(tzinfo=timezone.utc) if b.last_test_date.tzinfo is None else b.last_test_date
        r = calculate_recovery_readiness(
            backup_freshness_hours=max(0.0, (now - last_bk_dt).total_seconds() / 3600.0),
            target_rpo_hours=b.rpo_target_hours,
            verified=b.verified,
            last_test_days_ago=max(0.0, (now - last_test_dt).total_seconds() / 86400.0),
            rto_actual_hours=b.rto_actual_hours,
            rto_target_hours=b.rto_target_hours
        )
        total_r += r["readiness_index"]
    avg_readiness = round(total_r / max(1, len(backups)), 1) if backups else 72.0

    return {
        "system_status": "HEALTHY" if avg_risk < 75.0 else "ALERT",
        "last_event_seconds_ago": last_event_sec,
        "open_incidents_count": len(open_incidents),
        "total_incidents_count": len(incidents),
        "organization_risk_score": round(avg_risk, 1),
        "organization_risk_band": "CRITICAL" if avg_risk >= 75 else "HIGH" if avg_risk >= 50 else "MODERATE" if avg_risk >= 25 else "LOW",
        "recovery_readiness_score": avg_readiness,
        "incident_pressure": sev_counts,
        "risk_trend": [
            {"time": "08:00", "score": max(10, avg_risk - 18)},
            {"time": "10:00", "score": max(15, avg_risk - 12)},
            {"time": "12:00", "score": max(20, avg_risk - 6)},
            {"time": "14:00", "score": max(25, avg_risk - 2)},
            {"time": "16:00", "score": avg_risk}
        ]
    }
