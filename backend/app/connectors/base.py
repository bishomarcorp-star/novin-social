from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ConnectorPost:
    platform: str
    external_id: str
    text: str = ""
    author_platform_id: str | None = None
    author_username: str | None = None
    url: str | None = None
    published_at: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


class SocialConnector(ABC):
    platform: str

    @abstractmethod
    async def search_posts(self, query: str, limit: int = 20) -> list[ConnectorPost]:
        raise NotImplementedError
