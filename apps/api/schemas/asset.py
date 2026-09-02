from pydantic import BaseModel, ConfigDict
from typing import Optional

class AssetBase(BaseModel):
    asset_name: str
    asset_type: str
    criticality: str
    owner: str
    business_function: str
    data_sensitivity: str
    estimated_downtime_cost_per_hour: float = 1000.0
    user_blast_radius: int = 50

class AssetCreate(AssetBase):
    id: str

class AssetResponse(AssetBase):
    id: str
    model_config = ConfigDict(from_attributes=True)
