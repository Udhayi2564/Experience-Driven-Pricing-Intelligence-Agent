# src/tools/narrative.py
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import re

@tool
def product_narrative_analyzer_tool(description: str, title: str = "") -> dict:
    """
    Analyze product description for emotional and luxury indicators using Gemini.
    
    Args:
        description: Product description text
        title: Product title
    
    Returns:
        dict with narrative analysis scores
    """
    
    # Initialize Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3
    )
    
    # Luxury and emotional keyword detection
    luxury_keywords = [
        'handcrafted', 'artisan', 'bespoke', 'premium', 'exclusive',
        'limited edition', 'heritage', 'luxury', 'elegant', 'sophisticated',
        'finest', 'exquisite', 'curated', 'authentic', 'rare'
    ]
    
    emotional_keywords = [
        'love', 'feel', 'experience', 'journey', 'story', 'passion',
        'crafted with care', 'timeless', 'cherish', 'treasure', 'special',
        'meaningful', 'beautiful', 'stunning', 'gorgeous'
    ]
    
    craftsmanship_keywords = [
        'handmade', 'hand-stitched', 'artisan', 'crafted', 'skilled',
        'traditional', 'masterpiece', 'meticulously', 'attention to detail',
        'precision', 'craftsmanship', 'artistry'
    ]
    
    material_quality_keywords = [
        'genuine leather', 'pure silk', 'organic cotton', '100%', 'natural',
        'sustainable', 'premium materials', 'finest', 'quality',
        'authentic', 'real', 'pure', 'organic', 'eco-friendly'
    ]
    
    heritage_keywords = [
        'heritage', 'traditional', 'ancient', 'classic', 'vintage',
        'time-honored', 'legacy', 'generations', 'cultural', 'historic'
    ]
    
    sensory_keywords = [
        'soft', 'smooth', 'rich', 'luxurious feel', 'texture',
        'scent', 'aroma', 'fragrance', 'taste', 'touch', 'silky'
    ]
    
    text = (title + " " + description).lower()
    
    # Find matches
    luxury_found = [kw for kw in luxury_keywords if kw in text]
    emotional_found = [kw for kw in emotional_keywords if kw in text]
    craftsmanship_found = [kw for kw in craftsmanship_keywords if kw in text]
    material_found = [kw for kw in material_quality_keywords if kw in text]
    heritage_found = [kw for kw in heritage_keywords if kw in text]
    sensory_found = [kw for kw in sensory_keywords if kw in text]
    
    # Calculate scores
    luxury_score = min(100, len(luxury_found) * 15)
    emotional_score = min(100, len(emotional_found) * 12)
    craftsmanship_score = min(100, len(craftsmanship_found) * 18)
    material_quality_score = min(100, len(material_found) * 20)
    
    # Story strength combines all elements
    story_strength = (
        luxury_score * 0.25 +
        emotional_score * 0.30 +
        craftsmanship_score * 0.25 +
        material_quality_score * 0.20
    )
    
    return {
        "story_strength": round(story_strength, 2),
        "luxury_signals": luxury_found,
        "emotional_words": emotional_found,
        "craftsmanship_score": round(craftsmanship_score, 2),
        "material_quality_score": round(material_quality_score, 2),
        "heritage_indicators": heritage_found,
        "sensory_keywords": sensory_found,
        "experience_keywords": list(set(luxury_found + emotional_found))
    }
