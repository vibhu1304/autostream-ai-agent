def detect_intent(message: str) -> str:
    msg = message.lower()

    high_intent_keywords = [
        "buy", "purchase", "subscribe", "sign up", "get started", "i want"
    ]

    product_keywords = [
        "price", "pricing", "plan", "plans", "features", "cost", "subscription"
    ]

    greeting_keywords = ["hi", "hello", "hey"]

    if any(k in msg for k in high_intent_keywords):
        return "high_intent"

    if any(k in msg for k in greeting_keywords):
        return "greeting"

    if any(k in msg for k in product_keywords):
        return "product_query"

    return "product_query"
