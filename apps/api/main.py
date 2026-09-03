import os
import sys

# Ensure repository root and api directory are on sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
for p in [CURRENT_DIR, REPO_ROOT]:
    if p and p not in sys.path:
        sys.path.insert(0, p)

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from apps.api.core.config import settings
    from apps.api.core.database import engine, SessionLocal, Base
    from apps.api.routers import (
        telemetry,
        incidents,
        simulation,
        detections,
        behavior,
        recovery,
        ai,
        audit,
        settings as settings_router,
        stats
    )
    from apps.api.seeder.seed_db import seed_database
except ImportError:
    from core.config import settings
    from core.database import engine, SessionLocal, Base
    from routers import (
        telemetry,
        incidents,
        simulation,
        detections,
        behavior,
        recovery,
        ai,
        audit,
        settings as settings_router,
        stats
    )
    from seeder.seed_db import seed_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite tables & seed default baseline on startup
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_database(db)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware configuration - Supports production Vercel, Render, GitHub Pages, and local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Register API Routers
app.include_router(telemetry.router, prefix=settings.API_V1_STR)
app.include_router(incidents.router, prefix=settings.API_V1_STR)
app.include_router(simulation.router, prefix=settings.API_V1_STR)
app.include_router(detections.router, prefix=settings.API_V1_STR)
app.include_router(behavior.router, prefix=settings.API_V1_STR)
app.include_router(recovery.router, prefix=settings.API_V1_STR)
app.include_router(ai.router, prefix=settings.API_V1_STR)
app.include_router(audit.router, prefix=settings.API_V1_STR)
app.include_router(settings_router.router, prefix=settings.API_V1_STR)
app.include_router(stats.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "platform": "SentinelEdge",
        "title": "SentinelEdge Resilience API",
        "version": settings.VERSION,
        "status": "healthy",
        "docs": "/docs",
        "mode": "Research Prototype"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "engine": "FastAPI + Hybrid Detection Pipeline"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
