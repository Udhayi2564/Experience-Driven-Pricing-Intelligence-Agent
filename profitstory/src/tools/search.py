# src/tools/search.py
from langchain_core.tools import tool
from tavily import TavilyClient
import os

@tool
def web_search_tool(input: dict) -> dict:
    """
    Legal web search for Indian e-commerce products.
    
    Expected input:
        {
            "query": "water bottle",
            "top_k": 10
        }
    """

    query = input.get("query", "")
    top_k = input.get("top_k", 10)

    if not query:
        return {"error": "Query is missing"}

    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    enhanced_query = (
        f"{query} site:amazon.in OR site:flipkart.com OR site:myntra.com OR "
        f"site:ajio.com OR site:bigbasket.com OR site:nykaa.com OR site:snapdeal.com"
    )

    try:
        response = client.search(
            query=enhanced_query,
            max_results=top_k,
            search_depth="advanced",
            include_domains=[
                "amazon.in", "flipkart.com", "myntra.com", "ajio.com",
                "bigbasket.com", "nykaa.com", "snapdeal.com"
            ]
        )
    except Exception as e:
        return {"error": str(e)}

    results = []
    for item in response.get("results", []):
        results.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "snippet": item.get("content", ""),
            "domain": item.get("domain", "")
        })

    return {
        "results": results,
        "total_results": len(results)
    }
