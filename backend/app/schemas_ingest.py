from datetime import datetime
from pydantic import BaseModel, Field


class SocialCommentIn(BaseModel):
    external_id: str
    author_platform_id: str
    author_username: str | None = None
    text: str = ""
    published_at: datetime | None = None


class SocialPostIn(BaseModel):
    platform: str
    external_id: str
    author_platform_id: str | None = None
    author_username: str | None = None
    text: str = ""
    url: str | None = None
    published_at: datetime | None = None
    project_id: int | None = None
    comments: list[SocialCommentIn] = Field(default_factory=list)
