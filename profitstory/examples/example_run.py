# examples/example_run.py

import os
import sys
import json
from dotenv import load_dotenv

# Make sure Python can import src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agent.workflow import MarketIntelligenceWorkflow

load_dotenv()

def main():
    workflow = MarketIntelligenceWorkflow()

    print("=" * 60)
    print("Example 1: Stainless Steel Insulated Water Bottle")
    print("=" * 60)

    result1 = workflow.run("stainless steel insulated water bottle 24 hour temperature")
    print(json.dumps(result1, indent=2))

    print("\n" + "=" * 60)
    print("Example 2: Luxury Leather Bag")
    print("=" * 60)

    result2 = workflow.run("handcrafted genuine leather tote bag premium")
    print(json.dumps(result2, indent=2))

if __name__ == "__main__":
    main()
