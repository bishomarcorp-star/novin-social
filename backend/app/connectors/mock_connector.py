from .base import ConnectorPost, SocialConnector


class MockConnector(SocialConnector):
    platform = "mock"

    def __init__(self, posts: list[ConnectorPost] | None = None) -> None:
        self.posts = posts or []

    async def search_posts(self, query: str, limit: int = 20) -> list[ConnectorPost]:
        needle = query.strip().lower()
        matched = [
            post for post in self.posts
            if not needle or needle in post.text.lower()
        ]
        return matched[:limit]
