import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# 1. Config
write_file("apps/api/core/config.py", """import os

class Settings:
    PROJECT_NAME: str = "SentinelEdge"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "An Explainable AI-Assisted Cybersecurity and Recovery Readiness Platform for SMEs"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sentineledge.db")
    CORRELATION_WINDOW_MINUTES: int = int(os.getenv("CORRELATION_WINDOW_MINUTES", "30"))
    
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "local")
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
    AI_MODEL: str = os.getenv("AI_MODEL", "gpt-4o-mini")
    
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "https://sentineledge.onrender.com",
        "https://sentineledge-web.onrender.com",
        "*"
    ]

settings = Settings()
""")

# 2. Database
write_file("apps/api/core/database.py", """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from apps.api.core.config import settings

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""")

write_file("apps/api/core/__init__.py", """from apps.api.core.config import settings
from apps.api.core.database import Base, engine, SessionLocal, get_db
""")

# 3. Models
write_file("apps/api/models/event.py", """from sqlalchemy import Column, String, DateTime, JSON, BigInteger
from datetime import datetime, timezone
from apps.api.core.database import Base

class SecurityEvent(Base):
    __tablename__ = "security_events"

    id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    source = Column(String, index=True)
    user_id = Column(String, index=True, nullable=True)
    asset_id = Column(String, index=True, nullable=True)
    source_ip = Column(String, index=True, nullable=True)
    event_type = Column(String, index=True)
    action = Column(String, nullable=True)
    status = Column(String, index=True)
    endpoint = Column(String, nullable=True)
    device_id = Column(String, nullable=True)
    location = Column(String, nullable=True)
    bytes_transferred = Column(BigInteger, default=0)
    event_metadata = Column(JSON, default=dict)
""")

write_file("apps/api/models/incident.py", """from sqlalchemy import Column, String, Float, DateTime, JSON, Text
from datetime import datetime, timezone
from apps.api.core.database import Base

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String, index=True) # LOW, MEDIUM, HIGH, CRITICAL
    risk_score = Column(Float, default=0.0) # 0 - 100
    status = Column(String, default="OPEN", index=True) # OPEN, INVESTIGATING, MITIGATED, RESOLVED, FALSE_POSITIVE
    detected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    first_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    affected_asset = Column(String, index=True, nullable=True)
    affected_user = Column(String, index=True, nullable=True)
    attack_category = Column(String, index=True)
    business_impact = Column(String, default="MEDIUM")
    confidence = Column(Float, default=0.85)
    correlation_group = Column(String, index=True)
    event_ids = Column(JSON, default=list)
    risk_breakdown = Column(JSON, default=dict)
    ai_summary = Column(Text, nullable=True)
    ai_hypothesis = Column(Text, nullable=True)
    ai_alternative = Column(Text, nullable=True)
    ai_missing_evidence = Column(Text, nullable=True)
    recommended_action = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
""")

write_file("apps/api/models/asset.py", """from sqlalchemy import Column, String, Integer, Float
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
""")

write_file("apps/api/models/user.py", """from sqlalchemy import Column, String, Integer, Float, JSON
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
""")

write_file("apps/api/models/backup.py", """from sqlalchemy import Column, String, Float, DateTime, Boolean, Integer
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
""")

write_file("apps/api/models/audit.py", """from sqlalchemy import Column, String, DateTime, JSON, Text
from datetime import datetime, timezone
from apps.api.core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    actor = Column(String, nullable=False)
    role = Column(String, default="Analyst")
    action = Column(String, nullable=False)
    resource = Column(String, nullable=False)
    before_state = Column(JSON, nullable=True)
    after_state = Column(JSON, nullable=True)
    reason = Column(Text, nullable=False)
""")

write_file("apps/api/models/setting.py", """from sqlalchemy import Column, String, DateTime, Text
from datetime import datetime, timezone
from apps.api.core.database import Base

class SystemSetting(Base):
    __tablename__ = "system_settings"

    key = Column(String, primary_key=True, index=True)
    value = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
""")

write_file("apps/api/models/__init__.py", """from apps.api.models.event import SecurityEvent
from apps.api.models.incident import Incident
from apps.api.models.asset import Asset
from apps.api.models.user import UserEntity
from apps.api.models.backup import BackupInventory
from apps.api.models.audit import AuditLog
from apps.api.models.setting import SystemSetting
""")

print("Phase 1 core and models setup complete!")
