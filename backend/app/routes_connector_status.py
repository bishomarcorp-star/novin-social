from fastapi import APIRouter

from .config import settings


router = APIRouter(prefix="/connector-status", tags=["connector-status"])


@router.get("/x")
def x_status():
    return {
        "platform": "x",
        "configured": bool(settings.x_bearer_token),
        "search_url": settings.x_search_url,
        "timeout_seconds": settings.connector_timeout_seconds,
        "secret_exposed": False,
    }
