from app.hunter.normalization import normalize_text, compact_cta
from app.hunter.pattern_miner import mine_comment_patterns
from app.hunter.iran_detector import score_iran_relevance
from app.hunter.scoring import calculate_lead_score


def test_normalizes_persian_digits_and_arabic_chars():
    assert normalize_text("۱۲ كیف") == "12 کیف"


def test_compacts_cta_variants():
    assert compact_cta("عدد ۱۲ لطفا") == "12"
    assert compact_cta("12 کامنت کن") == "12"


def test_detects_repeated_cta_pattern():
    comments = ["12", "۱۲", "عدد 12", "12 لطفا", "اطلاعات", "12"]
    patterns = mine_comment_patterns(
        comments=comments,
        post_text="برای اطلاعات بیشتر عدد 12 را کامنت کنید",
        min_frequency=2,
        min_ratio=0.2,
    )
    assert patterns
    assert patterns[0].normalized_value == "12"
    assert patterns[0].frequency >= 5


def test_iran_relevance():
    result = score_iran_relevance(
        ["قیمت این سرمایه گذاری چند تومان است؟"],
        location="تهران",
    )
    assert result.score >= 70


def test_hot_lead_score():
    result = calculate_lead_score(
        iran_score=95,
        cta_matches=2,
        investment_or_product_context=True,
        asked_price=True,
        asked_how_to_buy=True,
        repeated_across_posts=3,
    )
    assert result.total_score >= 70
    assert result.level in {"HOT", "VERY_HOT"}
