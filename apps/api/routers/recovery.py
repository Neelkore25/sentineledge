from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from apps.api.core.database import get_db
from apps.api.models.backup import BackupInventory
from apps.api.engine.recovery import calculate_recovery_readiness

router = APIRouter(prefix="/recovery", tags=["recovery"])

@router.get("/inventory")
def get_backup_inventory(db: Session = Depends(get_db)):
    backups = db.query(BackupInventory).all()
    now = datetime.now(timezone.utc)
    results = []
    
    total_readiness = 0.0
    for b in backups:
        last_backup_dt = b.last_backup.replace(tzinfo=timezone.utc) if b.last_backup.tzinfo is None else b.last_backup
        last_test_dt = b.last_test_date.replace(tzinfo=timezone.utc) if b.last_test_date.tzinfo is None else b.last_test_date
        
        freshness_hrs = max(0.0, (now - last_backup_dt).total_seconds() / 3600.0)
        test_days_ago = max(0.0, (now - last_test_dt).total_seconds() / 86400.0)

        readiness = calculate_recovery_readiness(
            backup_freshness_hours=freshness_hrs,
            target_rpo_hours=b.rpo_target_hours,
            verified=b.verified,
            last_test_days_ago=test_days_ago,
            rto_actual_hours=b.rto_actual_hours,
            rto_target_hours=b.rto_target_hours
        )
        total_readiness += readiness["readiness_index"]

        results.append({
            "id": b.id,
            "asset_id": b.asset_id,
            "asset_name": b.asset_name,
            "last_backup": b.last_backup.isoformat(),
            "backup_type": b.backup_type,
            "backup_status": b.backup_status,
            "verified": b.verified,
            "retention_days": b.retention_days,
            "rto_target_hours": b.rto_target_hours,
            "rto_actual_hours": b.rto_actual_hours,
            "rpo_target_hours": b.rpo_target_hours,
            "rpo_actual_hours": b.rpo_actual_hours,
            "last_test_date": b.last_test_date.isoformat(),
            "test_result": b.test_result,
            "readiness": readiness
        })

    avg_readiness = round(total_readiness / max(1, len(results)), 1) if results else 75.0

    return {
        "overall_readiness_score": avg_readiness,
        "total_inventories": len(results),
        "items": results
    }
