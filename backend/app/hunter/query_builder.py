from dataclasses import dataclass


@dataclass
class BuiltQuery:
    query: str
    keywords: list[str]


def _quote(term: str) -> str:
    term = term.strip()
    if not term:
        return ""
    if " " in term:
        return f'"{term}"'
    return term


def build_x_discovery_query(
    positive_keywords: list[str],
    *,
    language: str | None = "fa",
    exclude_retweets: bool = True,
    max_keywords: int = 8,
) -> BuiltQuery:
    clean = []
    seen = set()

    for raw in positive_keywords:
        term = (raw or "").strip()
        key = term.casefold()
        if not term or key in seen:
            continue
        seen.add(key)
        clean.append(term)

    selected = clean[:max_keywords]
    if not selected:
        raise ValueError("at least one positive keyword is required")

    keyword_expr = " OR ".join(_quote(term) for term in selected)
    parts = [f"({keyword_expr})"]

    if language:
        parts.append(f"lang:{language}")

    if exclude_retweets:
        parts.append("-is:retweet")

    return BuiltQuery(
        query=" ".join(parts),
        keywords=selected,
    )


def build_x_replies_query(post_id: str) -> str:
    post_id = str(post_id).strip()
    if not post_id:
        raise ValueError("post_id is required")
    return f"conversation_id:{post_id} -is:retweet"
