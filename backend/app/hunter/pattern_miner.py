from collections import Counter
from dataclasses import dataclass
from .normalization import compact_cta, normalize_text


@dataclass
class PatternCandidate:
    normalized_value: str
    frequency: int
    ratio: float
    confidence: float
    samples: list[str]


CTA_HINTS = (
    "کامنت",
    "بفرست",
    "ارسال",
    "عدد",
    "کلمه",
    "اطلاعات",
    "لینک",
    "مشاوره",
)


def has_cta_hint(post_text: str) -> bool:
    normalized = normalize_text(post_text)
    return any(hint in normalized for hint in CTA_HINTS)


def mine_comment_patterns(
    comments: list[str],
    post_text: str = "",
    min_frequency: int = 3,
    min_ratio: float = 0.10,
) -> list[PatternCandidate]:
    cleaned = []
    originals: dict[str, list[str]] = {}

    for raw in comments:
        normalized = compact_cta(raw)
        if not normalized:
            continue
        cleaned.append(normalized)
        originals.setdefault(normalized, []).append(raw)

    if not cleaned:
        return []

    total = len(cleaned)
    counts = Counter(cleaned)
    cta_context_bonus = 0.15 if has_cta_hint(post_text) else 0.0

    results: list[PatternCandidate] = []
    for value, frequency in counts.most_common():
        ratio = frequency / total
        if frequency < min_frequency or ratio < min_ratio:
            continue

        frequency_score = min(0.55, ratio)
        repetition_score = min(0.25, frequency / max(total, 1))
        confidence = min(0.99, 0.20 + frequency_score + repetition_score + cta_context_bonus)

        results.append(
            PatternCandidate(
                normalized_value=value,
                frequency=frequency,
                ratio=round(ratio, 4),
                confidence=round(confidence, 4),
                samples=originals[value][:5],
            )
        )

    return results
