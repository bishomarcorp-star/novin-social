from app.hunter.project_matcher import score_project_match


def test_project_matcher_scores_relevant_text():
    result = score_project_match(
        ["برای خرید سهام و سرمایه گذاری اطلاعات میخوام"],
        ["سرمایه گذاری", "سهام", "خرید"],
        ["استخدام"],
    )
    assert result.score > 50
    assert "سهام" in result.matched_keywords


def test_project_matcher_penalizes_negative_keywords():
    result = score_project_match(
        ["استخدام در شرکت سرمایه گذاری"],
        ["سرمایه گذاری"],
        ["استخدام"],
    )
    assert result.score < 100
