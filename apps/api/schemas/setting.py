from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class SettingBase(BaseModel):
    key: str
    value: str
    description: Optional[str] = None

class SettingCreate(SettingBase):
    pass

class SettingUpdate(BaseModel):
    value: str
    description: Optional[str] = None

class SettingResponse(SettingBase):
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
