from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserEntityBase(BaseModel):
    username: str
    full_name: str
    role: str
    typical_login_start_hour: int = 9
    typical_login_end_hour: int = 18
    typical_locations: list[str] = ["Mumbai", "Bengaluru"]
    typical_devices: list[str] = ["Laptop-Corporate-01"]
    avg_daily_logins: float = 4.0
    avg_download_mb: float = 45.0
    download_history_json: list[float] = [40.0, 42.0, 45.0, 48.0, 44.0, 46.0, 43.0]

class UserEntityCreate(UserEntityBase):
    id: str

class UserEntityResponse(UserEntityBase):
    id: str
    model_config = ConfigDict(from_attributes=True)
