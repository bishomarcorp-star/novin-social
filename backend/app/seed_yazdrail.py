from sqlalchemy import select

from .db import SessionLocal
from .models import Project, Campaign


PROJECT_CONFIG = {
    "market": "iran",
    "language": "fa",
    "payment_currency": "IRR",
    "product_type": "share",
    "positive_keywords": [
        "سرمایه گذاری",
        "سهام",
        "خرید سهام",
        "فرصت سرمایه گذاری",
        "سرمایه",
        "اطلاعات",
        "لینک",
    ],
    "negative_keywords": [
        "استخدام",
        "خبر",
        "تحلیل خبری",
    ],
    "contact_mode": "permission_based",
}


def seed():
    db = SessionLocal()
    try:
        project = db.scalar(select(Project).where(Project.slug == "yazdrail"))
        if not project:
            project = Project(
                name="YazdRail",
                slug="yazdrail",
                industry="investment-rail",
                config=PROJECT_CONFIG,
            )
            db.add(project)
            db.commit()
            db.refresh(project)

        campaign = db.scalar(
            select(Campaign).where(
                Campaign.project_id == project.id,
                Campaign.name == "Share Sales Pilot",
            )
        )
        if not campaign:
            campaign = Campaign(
                project_id=project.id,
                name="Share Sales Pilot",
                target_country="IR",
                language="fa",
                conversion_goal="successful_share_purchase",
                targeting_config={
                    "min_iran_score": 70,
                    "min_lead_score": 51,
                    "pilot": True,
                },
            )
            db.add(campaign)
            db.commit()

        print({"project_id": project.id, "campaign": "Share Sales Pilot"})
    finally:
        db.close()


if __name__ == "__main__":
    seed()
