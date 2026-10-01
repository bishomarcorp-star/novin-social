from fastapi import APIRouter, HTTPException

from .connector_registry import get_x_connector
from .schemas_connectors import ConnectorSearchRequest


router = APIRouter(prefix="/connectors", tags=["connectors"])


@router.post("/x/search")
async def search_x(payload: ConnectorSearchRequest):
    try:
        connector = get_x_connector()
        posts = await connector.search_posts(payload.query, payload.limit)
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"X connector error: {exc}") from exc

    return {
        "platform": "x",
        "query": payload.query,
        "count": len(posts),
        "posts": [
            {
                "external_id": post.external_id,
                "text": post.text,
                "author_platform_id": post.author_platform_id,
                "author_username": post.author_username,
                "url": post.url,
                "published_at": post.published_at,
            }
            for post in posts
        ],
    }
