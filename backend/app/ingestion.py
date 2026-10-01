from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import Lead, LeadSignal, Pattern, SocialComment, SocialPost
from .schemas_ingest import SocialPostIn
from .hunter.normalization import compact_cta
from .hunter.pattern_miner import mine_comment_patterns
from .hunter.iran_detector import score_iran_relevance
from .hunter.scoring import calculate_lead_score


def get_or_create_post(db: Session, payload: SocialPostIn) -> SocialPost:
    post = db.scalar(
        select(SocialPost).where(
            SocialPost.platform == payload.platform,
            SocialPost.external_id == payload.external_id,
        )
    )
    if post:
        return post

    post = SocialPost(
        platform=payload.platform,
        external_id=payload.external_id,
        author_platform_id=payload.author_platform_id,
        author_username=payload.author_username,
        text=payload.text,
        url=payload.url,
        published_at=payload.published_at,
    )
    db.add(post)
    db.flush()
    return post


def get_or_create_lead(
    db: Session,
    *,
    platform: str,
    platform_user_id: str,
    username: str | None,
) -> Lead:
    lead = db.scalar(
        select(Lead).where(
            Lead.platform == platform,
            Lead.platform_user_id == platform_user_id,
        )
    )
    if lead:
        lead.last_seen = datetime.utcnow()
        if username and not lead.username:
            lead.username = username
        return lead

    lead = Lead(
        platform=platform,
        platform_user_id=platform_user_id,
        username=username,
    )
    db.add(lead)
    db.flush()
    return lead


def ingest_post(db: Session, payload: SocialPostIn) -> dict:
    post = get_or_create_post(db, payload)
    comments_added = 0

    for item in payload.comments:
        exists = db.scalar(
            select(SocialComment).where(
                SocialComment.platform == payload.platform,
                SocialComment.external_id == item.external_id,
            )
        )
        if exists:
            continue

        comment = SocialComment(
            post_id=post.id,
            platform=payload.platform,
            external_id=item.external_id,
            author_platform_id=item.author_platform_id,
            author_username=item.author_username,
            text=item.text,
            published_at=item.published_at,
        )
        db.add(comment)
        comments_added += 1

    db.flush()

    all_comments = db.scalars(
        select(SocialComment).where(SocialComment.post_id == post.id)
    ).all()
    comment_texts = [c.text or "" for c in all_comments]

    patterns = mine_comment_patterns(
        comments=comment_texts,
        post_text=post.text or "",
    )

    pattern_values = {p.normalized_value for p in patterns}
    patterns_saved = 0
    for candidate in patterns:
        existing_pattern = db.scalar(
            select(Pattern).where(
                Pattern.project_id == payload.project_id,
                Pattern.pattern_type == "CTA_COMMENT",
                Pattern.normalized_value == candidate.normalized_value,
            )
        )
        if existing_pattern:
            existing_pattern.frequency = max(existing_pattern.frequency, candidate.frequency)
            existing_pattern.confidence = max(existing_pattern.confidence, candidate.confidence)
        else:
            db.add(
                Pattern(
                    project_id=payload.project_id,
                    pattern_type="CTA_COMMENT",
                    raw_value=candidate.samples[0] if candidate.samples else candidate.normalized_value,
                    normalized_value=candidate.normalized_value,
                    meaning="REQUEST_MORE_INFORMATION",
                    frequency=candidate.frequency,
                    confidence=candidate.confidence,
                )
            )
            patterns_saved += 1

    leads_touched = 0
    signals_added = 0

    for comment in all_comments:
        normalized = compact_cta(comment.text)
        cta_match = normalized in pattern_values
        if not cta_match:
            continue

        lead = get_or_create_lead(
            db,
            platform=payload.platform,
            platform_user_id=comment.author_platform_id,
            username=comment.author_username,
        )

        iran = score_iran_relevance(
            [post.text or "", comment.text or ""]
        )
        score = calculate_lead_score(
            iran_score=iran.score,
            cta_matches=1,
            investment_or_product_context=True,
        )

        lead.iran_relevance_score = max(lead.iran_relevance_score, iran.score)
        lead.opportunity_score = max(lead.opportunity_score, score.opportunity_score)
        lead.total_lead_score = max(lead.total_lead_score, score.total_score)
        lead.status = score.level

        signal_exists = db.scalar(
            select(LeadSignal).where(
                LeadSignal.lead_id == lead.id,
                LeadSignal.source_url == (post.url or f"{payload.platform}:{post.external_id}"),
                LeadSignal.raw_text == (comment.text or ""),
            )
        )
        if not signal_exists:
            db.add(
                LeadSignal(
                    lead_id=lead.id,
                    project_id=payload.project_id,
                    source_type="CTA_COMMENT",
                    source_url=post.url or f"{payload.platform}:{post.external_id}",
                    raw_text=comment.text,
                    normalized_intent="REQUEST_MORE_INFORMATION",
                    confidence=max((p.confidence for p in patterns if p.normalized_value == normalized), default=0),
                )
            )
            signals_added += 1

        leads_touched += 1

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    return {
        "post_id": post.id,
        "comments_added": comments_added,
        "patterns_detected": len(patterns),
        "patterns_saved": patterns_saved,
        "leads_touched": leads_touched,
        "signals_added": signals_added,
        "patterns": [
            {
                "value": p.normalized_value,
                "frequency": p.frequency,
                "ratio": p.ratio,
                "confidence": p.confidence,
            }
            for p in patterns
        ],
    }
