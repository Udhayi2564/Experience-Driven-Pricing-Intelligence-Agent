# src/tools/marketing.py
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os

@tool
def marketing_justification_tool(
    product_title: str,
    suggested_price: float,
    experience_score: float,
    luxury_signals: list,
    craftsmanship_score: float,
    story_strength: float,
    brand_name: str
) -> str:
    """
    Generate marketing justification using Gemini 2.0 Flash.
    
    Args:
        product_title: Product name
        suggested_price: Recommended price
        experience_score: Experience score
        luxury_signals: List of luxury indicators
        craftsmanship_score: Craftsmanship score
        story_strength: Story strength score
        brand_name: Brand name
    
    Returns:
        str: Marketing justification text
    """
    
    # Initialize Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7
    )
    
    prompt = f"""Create a compelling 3-5 sentence marketing justification for this product's price.
Focus on experience, craftsmanship, emotional value, and quality.

Product: {product_title}
Brand: {brand_name}
Price: ₹{suggested_price}
Experience Score: {experience_score}/100
Craftsmanship Score: {craftsmanship_score}/100
Story Strength: {story_strength}/100
Luxury Signals: {', '.join(luxury_signals) if luxury_signals else 'None'}

Guidelines:
- Start with emotional/experiential value
- Highlight craftsmanship and quality
- Explain why price is fair for customers
- Use warm, premium language
- Don't mention scores or technical details
- Focus on the customer's experience

Write the justification:"""
    
    response = llm.invoke(prompt)
    return response.content.strip()
