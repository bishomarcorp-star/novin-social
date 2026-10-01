from app.hunter.query_builder import build_x_discovery_query


def test_yazdrail_style_query_is_generic():
    result = build_x_discovery_query([
        "سرمایه گذاری",
        "سهام",
        "فرصت سرمایه گذاری",
    ])
    assert "سرمایه گذاری" in result.query
    assert "سهام" in result.query
    assert "lang:fa" in result.query
