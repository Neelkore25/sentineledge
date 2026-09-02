from sqlalchemy import Column, String, Integer, Float, JSON
from apps.api.core.database import Base

class UserEntity(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    typical_login_start_hour = Column(Integer, default=9)
    typical_login_end_hour = Column(Integer, default=18)
    typical_locations = Column(JSON, default=lambda: ["Mumbai", "Bengaluru"])
    typical_devices = Column(JSON, default=lambda: ["Laptop-Corporate-01"])
    avg_daily_logins = Column(Float, default=4.0)
    avg_download_mb = Column(Float, default=45.0)
    download_history_json = Column(JSON, default=lambda: [40.0, 42.0, 45.0, 48.0, 44.0, 46.0, 43.0])
