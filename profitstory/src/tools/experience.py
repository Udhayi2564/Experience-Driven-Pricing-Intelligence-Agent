# src/tools/experience.py
from langchain_core.tools import tool

@tool
def experience_score_generator_tool(
    narrative_analysis: dict,
    review_insights: dict,
    brand_name: str,
    materials: list
) -> dict:
    """
    Generate comprehensive experience score from qualitative factors.
    
    Args:
        narrative_analysis: Output from narrative analyzer
        review_insights: Output from review intelligence
        brand_name: Product brand name
        materials: List of materials
    
    Returns:
        dict with experience scores
    """
    
    # Brand strength assessment
    premium_brands = [
        'forest essentials', 'fabindia', 'good earth', 'anita dongre',
        'raw mango', 'sabyasachi', 'milton', 'borosil', 'cello'
    ]
    
    brand_lower = brand_name.lower()
    brand_strength = 80 if any(pb in brand_lower for pb in premium_brands) else 50
    
    # Material premium assessment
    premium_materials = [
        'leather', 'silk', 'organic', 'handloom', 'khadi',
        'pure cotton', 'cashmere', 'wool', 'stainless steel', 'brass'
    ]
    
    materials_str = ' '.join(materials).lower() if materials else ""
    material_premium = min(100, sum(
        20 for pm in premium_materials if pm in materials_str
    ))
    
    # Extract scores from narrative analysis
    story_strength = narrative_analysis.get("story_strength", 50)
    craftsmanship_score = narrative_analysis.get("craftsmanship_score", 50)
    material_quality = narrative_analysis.get("material_quality_score", 50)
    
    # Luxury score
    luxury_signals_count = len(narrative_analysis.get("luxury_signals", []))
    luxury_score = min(100, luxury_signals_count * 15 + material_premium * 0.3)
    
    # Emotional index from sentiment
    sentiment_score = review_insights.get("sentiment_score", 50)
    emotional_words_count = len(narrative_analysis.get("emotional_words", []))
    emotional_index = (sentiment_score * 0.6 + emotional_words_count * 4)
    emotional_index = min(100, emotional_index)
    
    # Final experience score weighted formula
    experience_score = (
        story_strength * 0.25 +
        craftsmanship_score * 0.20 +
        brand_strength * 0.15 +
        luxury_score * 0.15 +
        emotional_index * 0.15 +
        material_premium * 0.10
    )
    
    return {
        "experience_score": round(experience_score, 2),
        "story_strength": round(story_strength, 2),
        "craftsmanship_score": round(craftsmanship_score, 2),
        "brand_strength": round(brand_strength, 2),
        "luxury_score": round(luxury_score, 2),
        "emotional_index": round(emotional_index, 2),
        "material_premium": round(material_premium, 2)
    }
