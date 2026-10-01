from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .db import SessionLocal
from .schemas_ingest import SocialPostIn
from .ingestion import ingest_post


router = APIRouter(prefix="/ingest", tags=["ingestion"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/post")
def ingest_social_post(payload: SocialPostIn, db: Session = Depends(get_db)):
    return ingest_post(db, payload)
