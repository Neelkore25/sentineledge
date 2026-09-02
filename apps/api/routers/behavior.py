from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.api.core.database import get_db
from apps.api.models.user import UserEntity
from apps.api.engine.anomaly import evaluate_user_behavior

router = APIRouter(prefix="/behavior", tags=["behavior"])

@router.get("/users")
def get_user_baselines(db: Session = Depends(get_db)):
    users = db.query(UserEntity).all()
    results = []
    for u in users:
        eval_res = evaluate_user_behavior(
            observed_download_mb=u.avg_download_mb * 1.2,
            observed_login_hour=11,
            user_baseline={
                "download_history_json": u.download_history_json,
                "typical_login_start_hour": u.typical_login_start_hour,
                "typical_login_end_hour": u.typical_login_end_hour
            }
        )
        results.append({
            "id": u.id,
            "username": u.username,
            "full_name": u.full_name,
            "role": u.role,
            "typical_login_hours": f"{u.typical_login_start_hour:02d}:00 - {u.typical_login_end_hour:02d}:00",
            "typical_locations": u.typical_locations,
            "typical_devices": u.typical_devices,
            "avg_daily_logins": u.avg_daily_logins,
            "avg_download_mb": u.avg_download_mb,
            "download_history": u.download_history_json,
            "baseline_evaluation": eval_res
        })
    return results
