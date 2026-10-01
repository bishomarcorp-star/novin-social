from dataclasses import dataclass
from .normalization import normalize_text


@dataclass
class ProjectMatch:
    score: float
    matched_keywords: list[str]
    matched_negative_keywords: list[str]


def score_project_match(
    text_samples: list[str],
    positive_keywords: list[str],
    negative_keywords: list[str] | None = None,
) -> ProjectMatch:
    normalized = normalize_text(" ".join(text_samples or []))
    positives = [normalize_text(k) for k in positive_keywords if normalize_text(k)]
    negatives = [normalize_text(k) for k in (negative_keywords or []) if normalize_text(k)]

    matched_pos = [k for k in positives if k in normalized]
    matched_neg = [k for k in negatives if k in normalized]

    if not positives:
        score = 0.0
    else:
        positive_ratio = len(set(matched_pos)) / len(set(positives))
        score = min(100.0, positive_ratio * 100)

    if matched_neg:
        score = max(0.0, score - min(60.0, len(set(matched_neg)) * 20.0))

    return ProjectMatch(
        score=round(score, 2),
        matched_keywords=sorted(set(matched_pos)),
        matched_negative_keywords=sorted(set(matched_neg)),
    )
