from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class BackupInventoryBase(BaseModel):
    asset_id: str
    asset_name: str
    backup_type: str = "Incremental"
    backup_status: str = "HEALTHY"
    verified: bool = True
    retention_days: int = 30
    rto_target_hours: float = 4.0
    rto_actual_hours: float = 3.2
    rpo_target_hours: float = 4.0
    rpo_actual_hours: float = 2.5
    test_result: str = "SUCCESS"

class BackupInventoryCreate(BackupInventoryBase):
    id: str
    last_backup: Optional[datetime] = None
    last_test_date: Optional[datetime] = None

class BackupInventoryResponse(BackupInventoryBase):
    id: str
    last_backup: datetime
    last_test_date: datetime
    model_config = ConfigDict(from_attributes=True)
