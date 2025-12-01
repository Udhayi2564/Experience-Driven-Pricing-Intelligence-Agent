# examples/example_run_custom.py

import sys
import os
import json

# Ensure src folder is importable (parent of examples/)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agent.workflow import MarketIntelligenceWorkflow


def main():

    print("============ Custom Product Pricing ============\n")

    # User input
    product_name = input("Enter product name: ").strip()
    initial_price = float(input("Enter initial price (INR): ").strip())
    description = input("Enter product description: ").strip()

    print("\nRunning Pricing Intelligence Engine...\n")

    workflow = MarketIntelligenceWorkflow()

    # Run the pricing engine
    result = workflow.run_custom(
        product_name=product_name,
        initial_price_inr=initial_price,
        description=description
    )

    # Pretty JSON output
    print("\n================= FINAL OUTPUT (JSON) =================")
    print(json.dumps(result, indent=4, ensure_ascii=False))
    print("=======================================================")


if __name__ == "__main__":
    main()
