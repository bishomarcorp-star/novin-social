from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .db import SessionLocal
from .models import Project
from .hunter.query_builder import build_x_discovery_query


router = APIRouter(prefix="/hunter-dry-run", tags=["hunter-dry-run"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/x/{project_id}")
def x_dry_run(project_id: int, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="project not found")

    config = project.config or {}
    keywords = config.get("positive_keywords") or []
    language = config.get("language") or "fa"

    try:
        built = build_x_discovery_query(
            keywords,
            language=language,
            exclude_retweets=True,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "project_id": project.id,
        "project_slug": project.slug,
        "platform": "x",
        "query": built.query,
        "keywords": built.keywords,
        "network_request_sent": False,
    }
