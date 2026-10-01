from fastapi import APIRouter

from .schemas import AnalyzePostRequest, LeadScoreRequest
from .hunter.pattern_miner import mine_comment_patterns
from .hunter.iran_detector import score_iran_relevance
from .hunter.scoring import calculate_lead_score


router = APIRouter(prefix="/hunter", tags=["hunter"])


@router.post("/analyze-post")
def analyze_post(payload: AnalyzePostRequest):
    patterns = mine_comment_patterns(
        comments=payload.comments,
        post_text=payload.post_text,
    )

    iran = score_iran_relevance(
        text_samples=[payload.post_text, *payload.comments],
        bio=payload.bio,
        location=payload.location,
    )

    return {
        "patterns": [
            {
                "normalized_value": p.normalized_value,
                "frequency": p.frequency,
                "ratio": p.ratio,
                "confidence": p.confidence,
                "samples": p.samples,
            }
            for p in patterns
        ],
        "iran_relevance": {
            "score": iran.score,
            "reasons": iran.reasons,
        },
    }


@router.post("/score-lead")
def score_lead(payload: LeadScoreRequest):
    result = calculate_lead_score(
        iran_score=payload.iran_score,
        cta_matches=payload.cta_matches,
        investment_or_product_context=payload.relevant_context,
        asked_price=payload.asked_price,
        asked_how_to_buy=payload.asked_how_to_buy,
        asked_for_link=payload.asked_for_link,
        repeated_across_posts=payload.repeated_across_posts,
    )

    return {
        "opportunity_score": result.opportunity_score,
        "total_score": result.total_score,
        "level": result.level,
        "reasons": result.reasons,
    }
