import re
from dataclasses import dataclass
from .normalization import normalize_text


@dataclass
class IranScore:
    score: float
    reasons: list[str]


PERSIAN_RE = re.compile(r"[\u0600-\u06FF]")
IRAN_HINTS = (
    "ایران", "تهران", "یزد", "مشهد", "اصفهان", "شیراز", "تبریز",
    "کرج", "قم", "اهواز", "رشت", "کرمان", "تومان", "ریال", "+98"
)


def score_iran_relevance(
    text_samples: list[str],
    bio: str | None = None,
    location: str | None = None,
) -> IranScore:
    score = 0.0
    reasons: list[str] = []

    combined = " ".join([*(text_samples or []), bio or "", location or ""])
    normalized = normalize_text(combined)

    if PERSIAN_RE.search(combined):
        score += 35
        reasons.append("persian_language")

    matched_hints = [hint for hint in IRAN_HINTS if hint in normalized]
    if matched_hints:
        score += min(35, 10 + 5 * len(set(matched_hints)))
        reasons.append("iran_context")

    if "+98" in combined or re.search(r"\b09\d{9}\b", normalized):
        score += 25
        reasons.append("iran_phone_signal")

    if "تومان" in normalized or "ریال" in normalized:
        score += 20
        reasons.append("iran_currency")

    return IranScore(score=min(100.0, score), reasons=reasons)
