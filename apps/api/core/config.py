import os

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
