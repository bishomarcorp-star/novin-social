from fastapi import APIRouter, HTTPException

from .config import settings
from .connector_registry import get_x_connector


router = APIRouter(prefix="/x-probe", tags=["x-probe"])


@router.get("")
async def probe_x():
    if not settings.x_bearer_token:
        return {
            "platform": "x",
            "configured": False,
            "reachable": False,
            "reason": "X_BEARER_TOKEN is not configured",
        }

    connector = get_x_connector()
    try:
        posts = await connector.search_posts("سرمایه گذاری lang:fa -is:retweet", 10)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"X live probe failed: {exc}") from exc

    return {
        "platform": "x",
        "configured": True,
        "reachable": True,
        "sample_count": len(posts),
        "secret_exposed": False,
    }
