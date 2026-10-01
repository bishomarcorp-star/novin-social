from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str
    slug: str
    industry: str | None = None
    organization_id: int | None = None
    config: dict = Field(default_factory=dict)


class CampaignCreate(BaseModel):
    project_id: int
    name: str
    target_country: str | None = None
    language: str | None = None
    conversion_goal: str | None = None
    targeting_config: dict = Field(default_factory=dict)
