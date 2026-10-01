from .config import settings
from .connectors.x_connector import XConnector


def get_x_connector() -> XConnector:
    return XConnector(
        bearer_token=settings.x_bearer_token or "",
        search_url=settings.x_search_url,
        timeout_seconds=settings.connector_timeout_seconds,
    )
