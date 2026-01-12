import json
from pathlib import Path

# Get absolute path to project root
BASE_DIR = Path(__file__).resolve().parent.parent
KB_PATH = BASE_DIR / "data" / "knowledge_base.json"

def load_knowledge():
    with open(KB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

KB = load_knowledge()

def retrieve_context(query: str) -> str:
    """
    Simple keyword-based retrieval over local knowledge base.
    This avoids embedding API quota issues while still ensuring
    grounded responses from structured KB (RAG).
    """
    query = query.lower()
    results = []

    # Retrieve plan info
    for plan in KB["plans"]:
        if (
            plan["name"].lower() in query
            or "price" in query
            or "pricing" in query
            or "plan" in query
            or "cost" in query
        ):
            text = f"""
Plan: {plan['name']}
Price: {plan['price']}
Videos: {plan['videos']}
Resolution: {plan['resolution']}
Features: {', '.join(plan['features']) if plan['features'] else 'None'}
"""
            results.append(text)

    # Retrieve policy info
    if "refund" in query or "policy" in query or "support" in query:
        policies = KB["policies"]
        policy_text = f"""
Refund Policy: {policies['refund']}
Support Policy: {policies['support']}
"""
        results.append(policy_text)

    # Fallback: return all KB if nothing matched
    if not results:
        for plan in KB["plans"]:
            results.append(
                f"{plan['name']} plan at {plan['price']} with {plan['videos']} and {plan['resolution']} resolution."
            )

    return "\n".join(results)
