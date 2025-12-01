# src/tools/trends.py
from langchain_core.tools import tool
from datetime import datetime
import calendar

@tool
def trend_intelligence_tool(input: dict) -> dict:
    """
    Detect seasonal patterns, festival demand, and trend boosts.

    Expected input:
    {
        "product_category": "...",
        "current_date": "YYYY-MM-DD" or None
    }
    """

    product_category = input.get("product_category", "").lower()
    current_date = input.get("current_date")

    if not current_date:
        current_date = datetime.now().strftime("%Y-%m-%d")

    date_obj = datetime.strptime(current_date, "%Y-%m-%d")
    month = date_obj.month

    # Indian festival calendar
    festivals = {
        1: [], 2: [], 3: ["Holi"], 4: [], 5: [], 6: [],
        7: [], 8: ["Raksha Bandhan"], 9: ["Ganesh Chaturthi"],
        10: ["Dussehra", "Diwali"], 11: ["Diwali"], 12: ["Christmas"]
    }

    trends_detected = []
    trend_boost_score = 0

    # FESTIVAL BOOST
    if festivals.get(month):
        trends_detected.append(f"Festival Season: {', '.join(festivals[month])}")
        trend_boost_score += 25

    # SUSTAINABILITY TREND
    sustainability_keywords = ["eco", "organic", "sustainable", "handmade", "natural"]
    if any(k in product_category for k in sustainability_keywords):
        trends_detected.append("Sustainability Demand Rising")
        trend_boost_score += 20

    # VIRAL TRENDS
    viral_indicators = []
    if "handmade" in product_category or "artisan" in product_category:
        viral_indicators.append("Support for Local Artisans Movement")
        trend_boost_score += 10

    return {
        "trends_detected": trends_detected,
        "trend_boost_score": min(100, trend_boost_score),
        "seasonal_factors": {
            "current_month": calendar.month_name[month],
            "festivals": festivals.get(month, []),
            "is_peak_season": trend_boost_score > 30
        },
        "viral_indicators": viral_indicators,
        "demand_forecast": (
            "high" if trend_boost_score > 50 else
            "medium" if trend_boost_score > 25 else
            "normal"
        ),
        "sustainability_trend": (
            75.0 if any(k in product_category for k in sustainability_keywords) else 45.0
        )
    }
