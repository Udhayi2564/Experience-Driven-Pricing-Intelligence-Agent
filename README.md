Experience-Driven Pricing Intelligence Agent for ProfitStory.ai
Overview
This project implements a production-ready AI pricing and competitive intelligence system that uses legal web scraping and AI agent orchestration to deliver real-time pricing recommendations for e-commerce brands. It is designed specifically for Indian marketplaces and leverages advanced language models to understand product storytelling, emotional value, and brand perception, going far beyond traditional, static dataset-based approaches.
Problem Statement
Most pricing systems either rely on static datasets (like CSVs) or only compare competitor prices without understanding the experience a product delivers. This leads to:
	Underpricing of premium, handcrafted, or story-driven products.
	Over-reliance on historical data instead of real-time market conditions.
	Lack of actionable insights from customer reviews and market trends.
Brands miss revenue opportunities and struggle to justify premium pricing to customers.
Objective
To build an AI agent that:
	Collects live product and pricing data from major Indian e-commerce platforms using legal, robots.txt-compliant scraping.
	Analyzes product narrative, emotional value, craftsmanship, and materials using an LLM.
	Mines customer reviews for love/hate patterns and price satisfaction.
	Detects seasonal and festival trends relevant to Indian markets.
	Computes an Experience Score and uses it with competitor prices and trends to recommend an optimal, profitable price.
	Generates a marketing-friendly price justification in natural language.
Approach / Methodology
	Real-Time Data Collection
	Use web search to discover relevant product pages (Amazon, Flipkart, Myntra, Ajio, BigBasket, Nykaa, Snapdeal).
	Scrape product pages legally, respecting robots.txt, to extract title, brand, description, specs, materials, images, and visible price.
	AI Tools / Modules
The system is decomposed into modular tools:
	Web Search Tool – finds product URLs from Indian e-commerce sites.
	Legal Scraper Tool – extracts product details and price while obeying robots.txt.
	Product Narrative Analyzer – detects luxury signals, emotional language, craftsmanship cues, material quality, and computes a story strength score.
	Review Intelligence Tool – analyzes reviews for love/complaint patterns, feature requests, sentiment, and price satisfaction.
	Competitor Pricing Tool – collects competitor products and prices, and computes a market baseline (min/avg/max).
	Trend Intelligence Tool – incorporates Indian seasons and festivals (Diwali, Holi, Raksha Bandhan, etc.) plus sustainability/eco-friendly trends to produce a trend boost score.
	Experience Score Generator – combines narrative, brand strength, materials, and sentiment into a unified 0–100 Experience Score.
	Pricing Engine – applies a transparent formula:
"Suggested Price"="Market Baseline"+"Experience Premium"+"Trend Boost"-"Competitor Pressure"+"Brand/Craftsmanship Bonus" 

	Marketing Justification Tool – uses an LLM to generate a 3–5 sentence explanation focusing on experience, quality, and fairness of the price.
	Agent Orchestration
	An AI agent orchestrates all tools in a sequential workflow:
	Search → 2) Scrape → 3) Narrative Analysis → 4) Competitor Pricing →
	Review Analysis → 6) Trend Detection → 7) Experience Score →
	Pricing Engine → 9) Marketing Justification → 10) JSON Output.
	The workflow is stateful and production-ready, with basic error handling and defaults if some data is missing.
Key Features
	No static dataset: Unlike a simple CSV-based project (e.g., product.csv), this system works with live market data for any new or existing product.
	Experience-Driven Pricing: Incorporates emotional value, storytelling, and craftsmanship instead of purely numeric factors.
	India-Focused Trends: Explicit modeling of Indian festival seasons and sustainability demand.
	Marketing-Ready Output: Generates final output as structured JSON plus a human-readable justification that can be used directly on product pages or internal reports.
	Scalable & Adaptable: New marketplaces, rules, or scoring dimensions can be added by plugging in additional tools or modifying config files, without redesigning the whole system.
Example Output (High Level)
For a product query like “stainless steel insulated water bottle, 24-hour hot/cold”:
	Market baseline price computed from Milton, Cello, Borosil, etc.
	Experience score based on material (304 stainless steel), insulation claims, eco-friendly positioning, and customer sentiment.
	Suggested price (e.g., ₹549) that is profitable, affordable, and volume-friendly compared to your starting price (₹220).
	JSON includes: product details, competitor list, market baseline, experience score, pricing formula breakdown, review insights, trend insights, final suggested price, and marketing justification.
Result / Impact
	Business: Helps brands set profitable yet competitive prices, justify premiums for high-experience products, and avoid underpricing.
	Technical: Demonstrates end-to-end capability in AI agents, legal web scraping, LLM integration, and real-time market intelligence, making the solution suitable for real-world deployment in e-commerce pricing and strategy teams.
Statement about the project:
My project uses legal web scraping and AI agent orchestration to deliver real-time pricing and competitive intelligence for e-commerce brands, leveraging the latest market data and advanced language models. This solution is scalable, adaptable, and ready for production, making it ideal for companies that need high-impact, automated intelligence—far beyond what static dataset analysis offers.

# Step 1: Set up environment
export GOOGLE_API_KEY="your_gemini_api_key"
export TAVILY_API_KEY="your_tavily_key"

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Run example
python examples/example_run.py
