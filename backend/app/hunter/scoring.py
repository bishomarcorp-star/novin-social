from dataclasses import dataclass


@dataclass
class LeadScore:
    opportunity_score: float
    total_score: float
    level: str
    reasons: list[str]


def calculate_lead_score(
    *,
    iran_score: float,
    cta_matches: int = 0,
    investment_or_product_context: bool = False,
    asked_price: bool = False,
    asked_how_to_buy: bool = False,
    asked_for_link: bool = False,
    repeated_across_posts: int = 0,
) -> LeadScore:
    opportunity = 0.0
    reasons: list[str] = []

    if investment_or_product_context:
        opportunity += 15
        reasons.append("relevant_context")

    if cta_matches > 0:
        opportunity += min(35, 20 + cta_matches * 5)
        reasons.append("cta_response")

    if repeated_across_posts > 1:
        opportunity += min(20, repeated_across_posts * 4)
        reasons.append("repeated_interest")

    if asked_price:
        opportunity += 15
        reasons.append("asked_price")

    if asked_how_to_buy:
        opportunity += 20
        reasons.append("asked_how_to_buy")

    if asked_for_link:
        opportunity += 25
        reasons.append("asked_for_link")

    opportunity = min(100.0, opportunity)
    total = round((opportunity * 0.7) + (iran_score * 0.3), 2)

    if total >= 86:
        level = "VERY_HOT"
    elif total >= 71:
        level = "HOT"
    elif total >= 51:
        level = "WARM"
    elif total >= 31:
        level = "INTERESTED"
    else:
        level = "COLD"

    return LeadScore(
        opportunity_score=round(opportunity, 2),
        total_score=total,
        level=level,
        reasons=reasons,
    )
