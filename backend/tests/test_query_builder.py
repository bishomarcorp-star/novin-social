from app.hunter.query_builder import (
    build_x_discovery_query,
    build_x_replies_query,
)


def test_builds_persian_discovery_query():
    result = build_x_discovery_query(
        ["سرمایه گذاری", "سهام", "سرمایه گذاری", "خرید سهام"],
        language="fa",
    )
    assert '"سرمایه گذاری"' in result.query
    assert "سهام" in result.query
    assert '"خرید سهام"' in result.query
    assert "lang:fa" in result.query
    assert "-is:retweet" in result.query
    assert len(result.keywords) == 3


def test_builds_replies_query():
    assert build_x_replies_query("123") == "conversation_id:123 -is:retweet"
