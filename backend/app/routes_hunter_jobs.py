from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .db import SessionLocal
from .schemas_hunter_jobs import XHunterRunRequest
from .x_hunter_pipeline import run_x_hunter_for_project


router = APIRouter(prefix="/hunter-jobs", tags=["hunter-jobs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/x/run")
async def run_x_hunter(payload: XHunterRunRequest, db: Session = Depends(get_db)):
    try:
        return await run_x_hunter_for_project(
            db,
            project_id=payload.project_id,
            post_limit=payload.post_limit,
            replies_per_post=payload.replies_per_post,
        )
    except ValueError as exc:
        detail = str(exc)
        status = 404 if detail == "project not found" else 400
        raise HTTPException(status_code=status, detail=detail) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"X hunter error: {exc}") from exc
