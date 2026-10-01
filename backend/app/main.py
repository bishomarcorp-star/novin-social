from fastapi import FastAPI

from .routes_hunter import router as hunter_router
from .routes_projects import router as projects_router
from .routes_ingest import router as ingest_router
from .routes_connectors import router as connectors_router
from .routes_hunter_jobs import router as hunter_jobs_router
from .routes_connector_status import router as connector_status_router
from .routes_hunter_dry_run import router as hunter_dry_run_router


app = FastAPI(title="Novin Social API", version="0.4.0")
app.include_router(hunter_router)
app.include_router(projects_router)
app.include_router(ingest_router)
app.include_router(connectors_router)
app.include_router(hunter_jobs_router)
app.include_router(connector_status_router)
app.include_router(hunter_dry_run_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "novin-social-api"}


@app.get("/")
def root():
    return {
        "name": "Novin Social",
        "version": "0.4.0",
        "mode": "multi-project social sales platform",
    }
