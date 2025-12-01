# src/tools/competitors.py
from langchain_core.tools import tool
from .search import web_search_tool
from .scraper import legal_web_scraper_tool

@tool
def competitor_pricing_tool(product_query: str, platforms: list = None) -> dict:
    """
    Search for competitor prices across Indian e-commerce platforms.
    
    Args:
        product_query: Product search query
        platforms: List of platforms to search
    
    Returns:
        dict with competitor pricing data
    """
    
    default_platforms = [
        "amazon.in", "flipkart.com", "myntra.com", 
        "ajio.com", "bigbasket.com", "nykaa.com", "snapdeal.com"
    ]
    
    platforms_to_search = platforms or default_platforms
    competitors = []
    
    # Search each platform
    for platform in platforms_to_search[:3]:  # Limit to 3 platforms for demo
        try:
            search_results = web_search_tool(
                query=f"{product_query} site:{platform}",
                top_k=2
            )
            
            for result in search_results["results"][:1]:  # Take first result per platform
                # Scrape product page
                product_data = legal_web_scraper_tool(result["url"])
                
                if product_data.get("price"):
                    competitors.append({
                        "title": product_data.get("title", result["title"]),
                        "price": product_data["price"],
                        "url": result["url"],
                        "platform": platform,
                        "brand": product_data.get("brand", "Unknown"),
                        "rating": None
                    })
        except Exception as e:
            continue
    
    if not competitors:
        # Return simulated data if scraping fails
        return {
            "competitors": [],
            "price_range": {"min": 0, "max": 0, "avg": 0},
            "total_found": 0
        }
    
    prices = [c["price"] for c in competitors]
    
    return {
        "competitors": competitors,
        "price_range": {
            "min": min(prices),
            "max": max(prices),
            "avg": sum(prices) / len(prices)
        },
        "total_found": len(competitors)
    }
