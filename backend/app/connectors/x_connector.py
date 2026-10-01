from __future__ import annotations

from typing import Any
import httpx

from .base import ConnectorPost, SocialConnector


class XConnector(SocialConnector):
    platform = "x"

    def __init__(
        self,
        *,
        bearer_token: str,
        search_url: str,
        timeout_seconds: float = 20.0,
    ) -> None:
        if not bearer_token:
            raise ValueError("X bearer token is required")
        if not search_url:
            raise ValueError("X search URL is required")

        self.bearer_token = bearer_token
        self.search_url = search_url
        self.timeout_seconds = timeout_seconds

    async def _search(self, query: str, limit: int = 20) -> list[ConnectorPost]:
        max_results = max(10, min(limit, 100))
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        params = {
            "query": query,
            "max_results": max_results,
            "tweet.fields": "id,text,author_id,created_at,lang,conversation_id,in_reply_to_user_id",
            "expansions": "author_id",
            "user.fields": "id,username,name,location,description",
        }

        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.get(self.search_url, headers=headers, params=params)
            response.raise_for_status()
            payload: dict[str, Any] = response.json()

        users = {
            str(user.get("id")): user
            for user in payload.get("includes", {}).get("users", [])
        }

        results: list[ConnectorPost] = []
        for item in payload.get("data", []):
            author_id = str(item.get("author_id")) if item.get("author_id") is not None else None
            user = users.get(author_id or "", {})
            post_id = str(item["id"])

            results.append(
                ConnectorPost(
                    platform=self.platform,
                    external_id=post_id,
                    text=item.get("text", ""),
                    author_platform_id=author_id,
                    author_username=user.get("username"),
                    url=f"https://x.com/{user.get('username')}/status/{post_id}" if user.get("username") else None,
                    published_at=item.get("created_at"),
                    raw={
                        "post": item,
                        "author": user,
                        "conversation_id": item.get("conversation_id"),
                        "in_reply_to_user_id": item.get("in_reply_to_user_id"),
                    },
                )
            )

        return results

    async def search_posts(self, query: str, limit: int = 20) -> list[ConnectorPost]:
        return await self._search(query=query, limit=limit)

    async def fetch_replies(self, post_id: str, limit: int = 100) -> list[ConnectorPost]:
        return await self._search(
            query=f"conversation_id:{post_id} -is:retweet",
            limit=limit,
        )
