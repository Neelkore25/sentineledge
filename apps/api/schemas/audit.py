from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Any

class AuditLogBase(BaseModel):
    actor: str
    role: str = "Analyst"
    action: str
    resource: str
    before_state: Optional[dict[str, Any]] = None
    after_state: Optional[dict[str, Any]] = None
    reason: str

class AuditLogCreate(AuditLogBase):
    id: Optional[str] = None
    timestamp: Optional[datetime] = None

class AuditLogResponse(AuditLogBase):
    id: str
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
