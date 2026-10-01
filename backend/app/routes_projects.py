from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .db import SessionLocal
from .models import Project, Campaign
from .schemas_projects import ProjectCreate, CampaignCreate


router = APIRouter(prefix="/projects", tags=["projects"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("")
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(Project).where(Project.slug == payload.slug))
    if existing:
        raise HTTPException(status_code=409, detail="project slug already exists")

    project = Project(
        name=payload.name,
        slug=payload.slug,
        industry=payload.industry,
        organization_id=payload.organization_id,
        config=payload.config,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return {"id": project.id, "name": project.name, "slug": project.slug}


@router.get("")
def list_projects(db: Session = Depends(get_db)):
    rows = db.scalars(select(Project).order_by(Project.id.desc())).all()
    return [
        {
            "id": row.id,
            "name": row.name,
            "slug": row.slug,
            "industry": row.industry,
            "active": row.active,
            "config": row.config,
        }
        for row in rows
    ]


@router.post("/campaigns")
def create_campaign(payload: CampaignCreate, db: Session = Depends(get_db)):
    project = db.get(Project, payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="project not found")

    campaign = Campaign(
        project_id=payload.project_id,
        name=payload.name,
        target_country=payload.target_country,
        language=payload.language,
        conversion_goal=payload.conversion_goal,
        targeting_config=payload.targeting_config,
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return {"id": campaign.id, "project_id": campaign.project_id, "name": campaign.name}
