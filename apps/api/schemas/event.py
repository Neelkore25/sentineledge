from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Any

class SecurityEventBase(BaseModel):
    source: str
    user_id: Optional[str] = None
    asset_id: Optional[str] = None
    source_ip: Optional[str] = None
    event_type: str
    action: Optional[str] = None
    status: str
    endpoint: Optional[str] = None
    device_id: Optional[str] = None
    location: Optional[str] = None
    bytes_transferred: int = 0
    event_metadata: dict[str, Any] = Field(default_factory=dict)

class SecurityEventCreate(SecurityEventBase):
    id: Optional[str] = None
    timestamp: Optional[datetime] = None

class SecurityEventResponse(SecurityEventBase):
    id: str
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
