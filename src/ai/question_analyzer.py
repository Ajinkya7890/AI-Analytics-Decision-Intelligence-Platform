import re


METRIC_PATTERNS = {
    "Revenue": [
        "revenue",
        "sales",
        "turnover",
        "sales value",
        "sales amount"
    ],
    "Freight Revenue": [
        "freight",
        "shipping revenue",
        "shipping cost",
        "freight value"
    ],
    "Average Order Value": [
        "average order value",
        "aov",
        "order value per order"
    ],
    "Order Count": [
        "orders",
        "order count",
        "number of orders",
        "how many orders"
    ],
    "Item Count": [
        "items",
        "item count",
        "number of items",
        "units",
        "units sold",
        "quantity sold"
    ],
    "Average Review Score": [
        "review score",
        "review rating",
        "average review",
        "rating",
        "ratings"
    ],
    "Average Delivery Days": [
        "delivery time",
        "delivery days",
        "delivery duration",
        "shipping time",
        "average delivery"
    ]
}


DIMENSION_PATTERNS = {
    "Product": [
        "product",
        "products",
        "category",
        "categories",
        "product category"
    ],
    "Seller": [
        "seller",
        "sellers",
        "vendor",
        "vendors"
    ],
    "Customer": [
        "customer",
        "customers",
        "buyer",
        "buyers"
    ],
    "Month": [
        "month",
        "monthly",
        "by month",
        "per month"
    ],
    "Year": [
        "year",
        "yearly",
        "annual",
        "annually",
        "by year",
        "per year"
    ]
}


def detect_intent(question_lower):
    """
    Detect the primary analytical intent from the question.
    """

    root_cause_patterns = [
        "why",
        "reason",
        "cause",
        "caused",
        "driver",
        "drivers",
        "decline reason",
        "growth reason"
    ]

    trend_patterns = [
        "trend",
        "over time",
        "monthly",
        "weekly",
        "daily",
        "month over month",
        "year over year",
        "yoy",
        "mom"
    ]

    comparison_patterns = [
        "compare",
        "comparison",
        "versus",
        "vs",
        "against",
        "difference between"
    ]

    ranking_patterns = [
        "top",
        "highest",
        "lowest",
        "best",
        "worst",
        "most",
        "least",
        "rank",
        "ranking"
    ]

    statistical_patterns = [
        "average",
        "mean",
        "median",
        "standard deviation",
        "variance",
        "distribution",
        "percentile"
    ]

    aggregation_patterns = [
        "how many",
        "count",
        "number of",
        "total",
        "sum",
        "overall",
        "by seller",
        "by product",
        "by category",
        "by customer",
        "grouped by",
        "per seller",
        "per product",
        "per category",
        "per customer"
    ]

    if any(pattern in question_lower for pattern in root_cause_patterns):
        return "root_cause"

    if any(pattern in question_lower for pattern in comparison_patterns):
        return "comparison"

    if any(pattern in question_lower for pattern in ranking_patterns):
        return "ranking"

    if any(pattern in question_lower for pattern in trend_patterns):
        return "trend_analysis"

    if any(pattern in question_lower for pattern in statistical_patterns):
        return "statistical"

    if any(pattern in question_lower for pattern in aggregation_patterns):
        return "aggregation"

    return "unknown"


def detect_metrics(question_lower):
    """
    Detect business metrics mentioned in the question.
    """

    metrics = []

    for metric, patterns in METRIC_PATTERNS.items():
        if any(pattern in question_lower for pattern in patterns):
            metrics.append(metric)

    return metrics


def detect_dimensions(question_lower):
    """
    Detect analytical dimensions mentioned in the question.
    """

    dimensions = []

    for dimension, patterns in DIMENSION_PATTERNS.items():
        if any(pattern in question_lower for pattern in patterns):
            dimensions.append(dimension)

    return dimensions


def detect_time_period(question):
    """
    Detect explicit years from the question.
    """

    years = re.findall(
        r"\b20\d{2}\b",
        question
    )

    return years if years else None


def analyze_question(question):
    """
    Convert a natural-language business question into
    a structured analytical representation.
    """

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    question_lower = question.lower()

    result = {
        "original_question": question,
        "intent": detect_intent(question_lower),
        "time_period": detect_time_period(question),
        "metrics": detect_metrics(question_lower),
        "dimensions": detect_dimensions(question_lower),
        "filters": []
    }

    return result