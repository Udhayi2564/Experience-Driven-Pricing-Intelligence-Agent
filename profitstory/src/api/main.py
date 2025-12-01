# src/api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent.workflow import run_pricing_agent
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="ProfitStory Pricing Intelligence API - Powered by Gemini 2.0 Flash",
    description="Experience-Driven Pricing Agent using Google Gemini",
    version="1.0.0"
)

class PricingRequest(BaseModel):
    product_query: str
    platform_filters: list = None
    
class PricingResponse(BaseModel):
    product_title: str
    brand: str
    suggested_price: float
    market_baseline: float
    experience_score: float
    confidence_level: str
    marketing_justification: str
    full_analysis: dict

@app.post("/api/v1/analyze-pricing", response_model=PricingResponse)
async def analyze_pricing(request: PricingRequest):
    """
    Analyze product and generate pricing recommendation using Gemini
    """
    try:
        result = run_pricing_agent(request.product_query)
        
        return PricingResponse(
            product_title=result["product_title"],
            brand=result["brand"],
            suggested_price=result["suggested_price"],
            market_baseline=result["market_baseline"],
            experience_score=result["experience_score"],
            confidence_level=result["confidence_level"],
            marketing_justification=result["marketing_justification"],
            full_analysis=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model": "gemini-2.0-flash",
        "framework": "LangChain + LangGraph"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
