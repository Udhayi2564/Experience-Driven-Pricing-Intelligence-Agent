# Step 1: Set up environment
export GOOGLE_API_KEY="your_gemini_api_key"
export TAVILY_API_KEY="your_tavily_key"

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Run example
python examples/example_run.py

# Step 4: Start API server
python src/api/main.py

# Step 5: Test API
curl -X POST "http://localhost:8000/api/v1/analyze-pricing" \
  -H "Content-Type: application/json" \
  -d '{"product_query": "stainless steel water bottle insulated"}'

& "C:/Users/Udhaya kumar KG/Desktop/profitstory.ai/profitstory/venv/Scripts/Activate.ps1"
(venv) PS C:\Users\Udhaya kumar KG\Desktop\profitstory.ai\profitstory> 