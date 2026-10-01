from pydantic import BaseModel, Field


class ConnectorSearchRequest(BaseModel):
    query: str
    limit: int = Field(default=20, ge=1, le=100)
