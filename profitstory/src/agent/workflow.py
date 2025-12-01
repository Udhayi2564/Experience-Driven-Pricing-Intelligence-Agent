# src/agent/workflow.py

from typing import TypedDict, Annotated, Sequence, Any, Dict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()

# ensure import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ---------------- TOOLS (correct signatures) ----------------
from src.tools.search import web_search_tool                 # expects { "input": { query, top_k }}
from src.tools.scraper import legal_web_scraper_tool         # expects { "input": { url }}
from src.tools.narrative import product_narrative_analyzer_tool   # expects { title, description }
from src.tools.reviews import review_intelligence_tool        # expects { "input": { reviews, max_reviews }}
from src.tools.competitors import competitor_pricing_tool     # expects { product_query, platforms }
from src.tools.trends import trend_intelligence_tool          # expects { "input": { product_category, current_date }}
from src.tools.experience import experience_score_generator_tool  # expects direct args (NO input)
from src.tools.pricing import pricing_engine_tool             # expects { "input": {...} }
from src.tools.marketing import marketing_justification_tool  # expects { "input": {...} }


# ---------------- STATE ----------------
class PricingAgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    product_query: str
    product_name: str
    initial_price_inr: float
    supplied_description: str
    search_results: dict
    product_data: dict
    narrative_analysis: dict
    competitor_data: dict
    review_insights: dict
    trend_insights: dict
    experience_score: dict
    pricing_result: dict
    marketing_justification: dict
    final_output: dict
    current_step: str


# ---------------- NODES ----------------

def search_product_node(state: PricingAgentState) -> PricingAgentState:
    state["search_results"] = web_search_tool.invoke({
        "input": {
            "query": state["product_query"],
            "top_k": 10
        }
    })
    return state


def scrape_product_node(state: PricingAgentState) -> PricingAgentState:

    results = state["search_results"].get("results", [])
    target_url = None

    for r in results:
        url = r.get("url", "")
        if any(x in url for x in ["amazon.in", "flipkart.com", "myntra.com"]):
            target_url = url
            break

    if not target_url and results:
        target_url = results[0]["url"]

    if target_url:
        state["product_data"] = legal_web_scraper_tool.invoke({
            "input": {"url": target_url}
        })
    else:
        state["product_data"] = {
            "title": state["product_name"],
            "description": state["supplied_description"],
            "brand": "Unknown",
            "materials": [],
            "price": state["initial_price_inr"],
            "scrape_allowed": False
        }

    return state


def analyze_narrative_node(state: PricingAgentState) -> PricingAgentState:

    pd = state["product_data"]

    combined_description = " ".join(filter(None, [
        pd.get("description", ""),
        state.get("supplied_description", "")
    ]))

    state["narrative_analysis"] = product_narrative_analyzer_tool.invoke({
        "title": pd.get("title", state["product_name"]),
        "description": combined_description
    })

    return state


def gather_competitor_data_node(state: PricingAgentState) -> PricingAgentState:

    state["competitor_data"] = competitor_pricing_tool.invoke({
        "product_query": state["product_query"],
        "platforms": None
    })

    return state


def analyze_reviews_node(state: PricingAgentState) -> PricingAgentState:

    reviews = [r.get("snippet", "") for r in state["search_results"].get("results", [])]

    state["review_insights"] = review_intelligence_tool.invoke({
        "input": {
            "reviews": reviews,
            "max_reviews": 50
        }
    })

    return state


def detect_trends_node(state: PricingAgentState) -> PricingAgentState:

    state["trend_insights"] = trend_intelligence_tool.invoke({
        "input": {
            "product_category": state["product_query"],
            "current_date": None
        }
    })

    return state


def calculate_experience_score_node(state: PricingAgentState) -> PricingAgentState:
    """MOST IMPORTANT FIX: NO `input:` wrapper"""

    pd = state["product_data"]

    state["experience_score"] = experience_score_generator_tool.invoke({
        "narrative_analysis": state["narrative_analysis"],
        "review_insights": state["review_insights"],
        "brand_name": pd.get("brand", "Unknown"),
        "materials": pd.get("materials", [])
    })

    return state


def calculate_pricing_node(state: PricingAgentState) -> PricingAgentState:

    cd = state["competitor_data"]
    es = state["experience_score"]
    ti = state["trend_insights"]

    baseline = cd.get("price_range", {}).get("avg") or state["initial_price_inr"] or 500

    competitor_prices = [c.get("price", baseline) for c in cd.get("competitors", [])]

    state["pricing_result"] = pricing_engine_tool.invoke({
        "input": {
            "market_baseline": baseline,
            "experience_score": es.get("experience_score", 50),
            "trend_boost_score": ti.get("trend_boost_score", 0),
            "competitor_prices": competitor_prices,
            "brand_strength": es.get("brand_strength", 30),
            "craftsmanship_score": es.get("craftsmanship_score", 20)
        }
    })

    return state


def rewrite_description_node(state: PricingAgentState) -> PricingAgentState:

    pd = state["product_data"]
    pr = state["pricing_result"]
    es = state["experience_score"]
    na = state["narrative_analysis"]

    justification = marketing_justification_tool.invoke({
            "product_title": pd.get("title", state["product_name"]),
            "suggested_price": pr.get("suggested_price"),
            "experience_score": es.get("experience_score", 50),
            "luxury_signals": na.get("luxury_signals", []),
            "craftsmanship_score": es.get("craftsmanship_score", 0),
            "story_strength": es.get("story_strength", 0),
            "brand_name": pd.get("brand", state["product_name"])
    })

    rewritten = justification.get("marketing_copy") if isinstance(justification, dict) else justification

    state["product_data"]["rewritten_description"] = rewritten
    state["marketing_justification"] = {"marketing_copy": rewritten}

    return state


def compile_output_node(state: PricingAgentState) -> PricingAgentState:

    final = {
        "product_title": state["product_data"].get("title"),
        "brand": state["product_data"].get("brand"),
        "rewritten_description": state["product_data"].get("rewritten_description"),
        "competitor_prices": state["competitor_data"].get("competitors", []),
        "experience_score": state["experience_score"].get("experience_score"),
        "trend_insights": state["trend_insights"].get("trends_detected", []),
        "pricing_result": state["pricing_result"],
        "suggested_price": state["pricing_result"].get("suggested_price"),
        "marketing_justification": state["marketing_justification"],
    }

    state["final_output"] = final
    return state


# ---------------- GRAPH ----------------

def create_pricing_agent():

    workflow = StateGraph(PricingAgentState)

    workflow.add_node("search_product", search_product_node)
    workflow.add_node("scrape_product", scrape_product_node)
    workflow.add_node("analyze_narrative", analyze_narrative_node)
    workflow.add_node("gather_competitors", gather_competitor_data_node)
    workflow.add_node("analyze_reviews", analyze_reviews_node)
    workflow.add_node("detect_trends", detect_trends_node)
    workflow.add_node("calculate_experience", calculate_experience_score_node)
    workflow.add_node("calculate_pricing", calculate_pricing_node)
    workflow.add_node("rewrite_description", rewrite_description_node)
    workflow.add_node("compile_output", compile_output_node)

    workflow.set_entry_point("search_product")

    workflow.add_edge("search_product", "scrape_product")
    workflow.add_edge("scrape_product", "analyze_narrative")
    workflow.add_edge("analyze_narrative", "gather_competitors")
    workflow.add_edge("gather_competitors", "analyze_reviews")
    workflow.add_edge("analyze_reviews", "detect_trends")
    workflow.add_edge("detect_trends", "calculate_experience")
    workflow.add_edge("calculate_experience", "calculate_pricing")
    workflow.add_edge("calculate_pricing", "rewrite_description")
    workflow.add_edge("rewrite_description", "compile_output")
    workflow.add_edge("compile_output", END)

    return workflow.compile()


# ---------------- RUNNERS ----------------

def run_pricing_agent(product_query: str, product_name: str, initial_price_inr: float, supplied_description: str):

    agent = create_pricing_agent()

    state = {
        "messages": [HumanMessage(content=f"Analyze pricing for: {product_query}")],
        "product_query": product_query,
        "product_name": product_name,
        "initial_price_inr": float(initial_price_inr),
        "supplied_description": supplied_description,
        "search_results": {},
        "product_data": {},
        "narrative_analysis": {},
        "competitor_data": {},
        "review_insights": {},
        "trend_insights": {},
        "experience_score": {},
        "pricing_result": {},
        "marketing_justification": {},
        "final_output": {},
        "current_step": "start"
    }

    result = agent.invoke(state)
    return result["final_output"]


class MarketIntelligenceWorkflow:

    def run(self, product_query: str):
        return run_pricing_agent(product_query, product_query, 0, "")

    def run_custom(self, product_name: str, initial_price_inr: float, description: str):
        query = f"{product_name} {description}"
        return run_pricing_agent(query, product_name, initial_price_inr, description)
