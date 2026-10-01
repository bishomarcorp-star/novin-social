from pydantic import BaseModel, Field


class XHunterRunRequest(BaseModel):
    project_id: int
    post_limit: int = Field(default=20, ge=10, le=100)
    replies_per_post: int = Field(default=100, ge=10, le=100)
