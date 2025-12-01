from langchain_core.tools import tool
import statistics

@tool
def pricing_engine_tool(input: dict) -> dict:
    """
    Pricing engine with:
    - Market baseline fallback
    - Experience-driven boosting
    - Trend + brand + craftsmanship scoring
    - Dynamic multiplier (MAX 10x)
    """

    # --------------------------  
    # INPUT  
    # --------------------------
    market_baseline = input.get("market_baseline", 500)
    experience = input.get("experience_score", 50)
    trend = input.get("trend_boost_score", 10)
    competitor_prices = input.get("competitor_prices", [])
    brand_strength = input.get("brand_strength", 0)
    craftsmanship = input.get("craftsmanship_score", 0)

    # --------------------------  
    # COMPETITOR PRICE LOGIC  
    # --------------------------
    if competitor_prices:
        competitor_avg = statistics.mean(competitor_prices)
        competitor_adjustment = competitor_avg * 0.12  # 12% boost
        baseline = competitor_avg
    else:
        competitor_adjustment = 0

        # Smart fallback baseline
        if market_baseline <= 0:
            baseline = 999  # Higher fallback
        else:
            baseline = market_baseline

    # --------------------------  
    # EXPERIENCE PREMIUM  
    # --------------------------
    experience_premium = (experience / 100) * (baseline * 0.4)

    # --------------------------  
    # BRAND BONUS  
    # --------------------------
    brand_bonus = (brand_strength / 100) * (baseline * 0.25)

    # --------------------------  
    # CRAFTSMANSHIP BONUS  
    # --------------------------
    craftsmanship_bonus = craftsmanship * 10

    # --------------------------  
    # TREND BOOST  
    # --------------------------
    trend_boost = (trend / 100) * (baseline * 0.25)

    # --------------------------  
    # BASE PRICE BEFORE MULTIPLIER  
    # --------------------------
    pre_multiplier_price = (
        baseline
        + experience_premium
        + trend_boost
        + competitor_adjustment
        + brand_bonus
        + craftsmanship_bonus
    )

    # ============================================================
    # DYNAMIC MULTIPLIER (MAX 10X)
    # ============================================================
    if experience < 40:
        multiplier = 3
    elif experience < 70:
        multiplier = 5
    elif experience < 90:
        multiplier = 7
    else:
        multiplier = 10   # premium category

    multiplier = min(multiplier, 10)  # NEVER exceed 10×

    # Final price AFTER multiplier
    final_price = int(pre_multiplier_price * multiplier)

    # --------------------------  
    # CONFIDENCE MODEL  
    # --------------------------
    score = 0

    # Competitors
    if len(competitor_prices) >= 3:
        score += 40
    elif len(competitor_prices) >= 1:
        score += 25
    else:
        score += 10

    # Experience score
    if experience >= 70:
        score += 30
    elif experience >= 50:
        score += 20
    else:
        score += 10

    # Trend
    if trend >= 50:
        score += 20
    elif trend >= 20:
        score += 10
    else:
        score += 5

    # Brand
    if brand_strength >= 60:
        score += 10
    elif brand_strength >= 20:
        score += 5

    # Confidence level
    if score >= 80:
        confidence_level = "high"
    elif score >= 50:
        confidence_level = "medium"
    else:
        confidence_level = "low"

    # Market position
    if competitor_prices:
        avg = statistics.mean(competitor_prices)
        if final_price < avg * 0.9:
            price_position = "below_market"
        elif final_price > avg * 1.2:
            price_position = "above_market"
        else:
            price_position = "competitive"
    else:
        price_position = "estimated"

    # --------------------------  
    # RETURN JSON RESULT  
    # --------------------------
    return {
        "suggested_price": final_price,
        "market_baseline": baseline,
        "experience_premium": round(experience_premium, 2),
        "trend_boost": round(trend_boost, 2),
        "competitor_adjustment": round(competitor_adjustment, 2),
        "brand_bonus": round(brand_bonus, 2),
        "craftsmanship_bonus": craftsmanship_bonus,
        "dynamic_multiplier": multiplier,
        "pre_multiplier_price": int(pre_multiplier_price),
        "confidence_level": confidence_level,
        "price_position": price_position
    }
