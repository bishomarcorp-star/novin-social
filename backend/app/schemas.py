from pydantic import BaseModel, Field


class AnalyzePostRequest(BaseModel):
    post_text: str = ""
    comments: list[str] = Field(default_factory=list)
    bio: str | None = None
    location: str | None = None


class LeadScoreRequest(BaseModel):
    iran_score: float = 0
    cta_matches: int = 0
    relevant_context: bool = False
    asked_price: bool = False
    asked_how_to_buy: bool = False
    asked_for_link: bool = False
    repeated_across_posts: int = 0
