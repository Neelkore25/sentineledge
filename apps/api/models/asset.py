from sqlalchemy import Column, String, Integer, Float
from apps.api.core.database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(String, primary_key=True, index=True)
    asset_name = Column(String, nullable=False)
    asset_type = Column(String, nullable=False)
    criticality = Column(String, nullable=False) # Tier 1, Tier 2, Tier 3, Tier 4
    owner = Column(String, nullable=False)
    business_function = Column(String, nullable=False)
    data_sensitivity = Column(String, nullable=False) # PII, Financial, Operational, Public
    estimated_downtime_cost_per_hour = Column(Float, default=1000.0)
    user_blast_radius = Column(Integer, default=50)
