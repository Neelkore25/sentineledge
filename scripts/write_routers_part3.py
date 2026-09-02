import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# 7. AI Investigation Router
write_file("apps/api/routers/ai.py", """from fastapi import APIRouter, Depends, HTTPException, Body
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
""")

# 8. Audit Log Router
write_file("apps/api/routers/audit.py", """from fastapi import APIRouter, Depends
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
""")

# 9. Settings Router
write_file("apps/api/routers/settings.py", """from fastapi import APIRouter, Depends, HTTPException, Body
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
""")

# 10. Stats Overview Router
write_file("apps/api/routers/stats.py", """from fastapi import APIRouter, Depends
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
""")

write_file("apps/api/routers/__init__.py", "# Routers module\n")

# 11. FastAPI Main Application
write_file("apps/api/main.py", """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apps.api.core.config import settings
from apps.api.core.database import Base, engine, SessionLocal
from apps.api.seeder.seed_db import seed_database
from apps.api.routers import (
    telemetry, incidents, simulation, detections, behavior,
    recovery, ai, audit, settings as api_settings, stats
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(telemetry.router, prefix=settings.API_V1_STR)
app.include_router(incidents.router, prefix=settings.API_V1_STR)
app.include_router(simulation.router, prefix=settings.API_V1_STR)
app.include_router(detections.router, prefix=settings.API_V1_STR)
app.include_router(behavior.router, prefix=settings.API_V1_STR)
app.include_router(recovery.router, prefix=settings.API_V1_STR)
app.include_router(ai.router, prefix=settings.API_V1_STR)
app.include_router(audit.router, prefix=settings.API_V1_STR)
app.include_router(api_settings.router, prefix=settings.API_V1_STR)
app.include_router(stats.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "platform": settings.PROJECT_NAME,
        "tagline": "Detect clearly. Respond deliberately. Recover ready.",
        "version": settings.VERSION,
        "status": "operational",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apps.api.main:app", host="0.0.0.0", port=8000, reload=True)
""")

print("Part 3 routers and main app written.")
