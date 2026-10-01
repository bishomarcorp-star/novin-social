from fastapi import FastAPI

from .routes_hunter import router as hunter_router
from .routes_projects import router as projects_router
from .routes_ingest import router as ingest_router
from .routes_connectors import router as connectors_router


app = FastAPI(title="Novin Social API", version="0.2.0")
app.include_router(hunter_router)
app.include_router(projects_router)
app.include_router(ingest_router)
app.include_router(connectors_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "novin-social-api"}


@app.get("/")
def root():
    return {
        "name": "Novin Social",
        "version": "0.2.0",
        "mode": "multi-project social sales platform",
    }
