import re


def analyze_question(question):
    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    question_lower = question.lower()

    intent = "unknown"

    if any(word in question_lower for word in [
        "why",
        "reason",
        "cause",
        "caused"
    ]):
        intent = "root_cause"

    elif any(word in question_lower for word in [
        "trend",
        "over time",
        "monthly",
        "weekly",
        "daily"
    ]):
        intent = "trend_analysis"

    elif any(word in question_lower for word in [
        "compare",
        "comparison",
        "versus",
        "vs"
    ]):
        intent = "comparison"

    elif any(word in question_lower for word in [
        "how many",
        "count",
        "number of"
    ]):
        intent = "aggregation"

    elif any(word in question_lower for word in [
        "average",
        "mean",
        "median"
    ]):
        intent = "statistical"

    elif any(word in question_lower for word in [
        "top",
        "highest",
        "lowest",
        "best",
        "worst"
    ]):
        intent = "ranking"

    result = {
        "original_question": question,
        "intent": intent,
        "time_period": None,
        "metrics": [],
        "dimensions": [],
        "filters": []
    }

    # Detect common metrics
    if "revenue" in question_lower:
        result["metrics"].append("Revenue")

    if "freight" in question_lower:
        result["metrics"].append("Freight Revenue")

    if "order value" in question_lower or "aov" in question_lower:
        result["metrics"].append("Average Order Value")

    if "orders" in question_lower:
        result["metrics"].append("Order Count")

    if "items" in question_lower:
        result["metrics"].append("Item Count")

    if "review" in question_lower or "rating" in question_lower:
        result["metrics"].append("Average Review Score")

    if "delivery" in question_lower:
        result["metrics"].append("Average Delivery Days")

    # Detect dimensions
    if "product" in question_lower or "category" in question_lower:
        result["dimensions"].append("Product")

    if "seller" in question_lower:
        result["dimensions"].append("Seller")

    if "customer" in question_lower:
        result["dimensions"].append("Customer")

    if any(word in question_lower for word in [
        "month",
        "monthly"
    ]):
        result["dimensions"].append("Month")

    if any(word in question_lower for word in [
        "year",
        "yearly",
        "annual"
    ]):
        result["dimensions"].append("Year")

    # Detect years
    years = re.findall(r"\b20\d{2}\b", question)

    if years:
        result["time_period"] = years

    return result