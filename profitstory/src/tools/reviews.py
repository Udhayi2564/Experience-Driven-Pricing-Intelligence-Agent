# src/tools/reviews.py
from langchain_core.tools import tool
from transformers import pipeline
import re

@tool
def review_intelligence_tool(input: dict) -> dict:
    """
    Analyze customer review patterns.
    
    Expected input:
    {
        "reviews": [...],
        "max_reviews": 50
    }
    """

    reviews = input.get("reviews", [])
    max_reviews = input.get("max_reviews", 50)

    if not reviews:
        return {
            "sentiment_score": 50,
            "love_patterns": [],
            "complaint_patterns": [],
            "feature_requests": []
        }

    sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )

    sentiments = []
    love_patterns = []
    complaint_patterns = []
    feature_requests = []

    positive_keywords = ['love', 'amazing', 'excellent', 'perfect', 'best',
                         'great', 'wonderful', 'beautiful', 'quality']
    negative_keywords = ['disappointed', 'poor', 'bad', 'waste', 'terrible',
                         'cheap', 'fake', 'worst', 'defective']
    request_patterns = [
        r'wish it had', r'would be better if', r'should have',
        r'needs', r'could improve', r'missing'
    ]

    for review in reviews[:max_reviews]:
        sentiment = sentiment_analyzer(str(review)[:512])[0]
        sentiments.append(1.0 if sentiment['label'] == 'POSITIVE' else 0.0)

        rev = str(review).lower()

        # positive patterns
        for kw in positive_keywords:
            if kw in rev:
                match = re.search(f".{{0,50}}{kw}.{{0,50}}", rev)
                if match:
                    love_patterns.append(match.group(0).strip())

        # negative patterns
        for kw in negative_keywords:
            if kw in rev:
                match = re.search(f".{{0,50}}{kw}.{{0,50}}", rev)
                if match:
                    complaint_patterns.append(match.group(0).strip())

        # feature request patterns
        for pattern in request_patterns:
            matches = re.finditer(pattern + r".{0,80}", rev)
            for m in matches:
                feature_requests.append(m.group(0).strip())

    # price perception
    price_mentions = [r for r in reviews if any(
        w in str(r).lower() for w in ["price", "cost", "expensive", "cheap", "value"]
    )]

    price_positive = sum(
        1 for r in price_mentions if any(
            w in str(r).lower() for w in ["worth", "value", "reasonable", "fair"]
        )
    )

    if len(price_mentions) == 0:
        price_satisfaction = "medium"
    else:
        ratio = price_positive / len(price_mentions)
        price_satisfaction = (
            "high" if ratio > 0.6 else
            "medium" if ratio > 0.3 else
            "low"
        )

    sentiment_score = sum(sentiments) / len(sentiments) * 100 if sentiments else 50

    return {
        "love_patterns": list(set(love_patterns))[:10],
        "complaint_patterns": list(set(complaint_patterns))[:10],
        "feature_requests": list(set(feature_requests))[:10],
        "sentiment_score": round(sentiment_score, 2),
        "price_satisfaction": price_satisfaction,
        "total_reviews_analyzed": len(reviews[:max_reviews]),
        "positive_ratio": round(sum(sentiments) / len(sentiments), 2) if sentiments else 0.5
    }
