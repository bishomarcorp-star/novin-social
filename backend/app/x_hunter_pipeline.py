from datetime import datetime
from sqlalchemy.orm import Session

from .connector_registry import get_x_connector
from .hunter.query_builder import build_x_discovery_query
from .ingestion import ingest_post
from .models import Project
from .schemas_ingest import SocialCommentIn, SocialPostIn


async def run_x_hunter_for_project(
    db: Session,
    *,
    project_id: int,
    post_limit: int = 20,
    replies_per_post: int = 100,
) -> dict:
    project = db.get(Project, project_id)
    if not project:
        raise ValueError("project not found")

    config = project.config or {}
    keywords = config.get("positive_keywords") or []
    language = config.get("language") or "fa"

    built = build_x_discovery_query(
        keywords,
        language=language,
        exclude_retweets=True,
    )

    connector = get_x_connector()
    posts = await connector.search_posts(built.query, post_limit)

    results = []
    for post in posts:
        replies = await connector.fetch_replies(
            post.external_id,
            limit=replies_per_post,
        )

        comments = []
        for reply in replies:
            if reply.external_id == post.external_id:
                continue

            comments.append(
                SocialCommentIn(
                    external_id=reply.external_id,
                    author_platform_id=reply.author_platform_id or "unknown",
                    author_username=reply.author_username,
                    text=reply.text,
                    published_at=_parse_dt(reply.published_at),
                )
            )

        payload = SocialPostIn(
            platform="x",
            external_id=post.external_id,
            author_platform_id=post.author_platform_id,
            author_username=post.author_username,
            text=post.text,
            url=post.url,
            published_at=_parse_dt(post.published_at),
            project_id=project.id,
            comments=comments,
        )

        ingest_result = ingest_post(db, payload)
        results.append(
            {
                "post_id": post.external_id,
                "post_url": post.url,
                "replies_fetched": len(comments),
                "ingestion": ingest_result,
            }
        )

    return {
        "project_id": project.id,
        "project_slug": project.slug,
        "query": built.query,
        "keywords": built.keywords,
        "posts_fetched": len(posts),
        "results": results,
    }


def _parse_dt(value: str | None):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
