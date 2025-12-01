# Step 1: Set up environment
export GOOGLE_API_KEY="your_gemini_api_key"
export TAVILY_API_KEY="your_tavily_key"

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Run example
python examples/example_run.py

# Step 4: Start API server
python src/api/main.py

