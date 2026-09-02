from sqlalchemy import Column, String, Float, DateTime, Boolean, Integer
from datetime import datetime, timezone
from apps.api.core.database import Base

class BackupInventory(Base):
    __tablename__ = "backup_inventories"

    id = Column(String, primary_key=True, index=True)
    asset_id = Column(String, index=True, nullable=False)
    asset_name = Column(String, nullable=False)
    last_backup = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    backup_type = Column(String, default="Incremental")
    backup_status = Column(String, default="HEALTHY")
    verified = Column(Boolean, default=True)
    retention_days = Column(Integer, default=30)
    rto_target_hours = Column(Float, default=4.0)
    rto_actual_hours = Column(Float, default=3.2)
    rpo_target_hours = Column(Float, default=4.0)
    rpo_actual_hours = Column(Float, default=2.5)
    last_test_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    test_result = Column(String, default="SUCCESS")
