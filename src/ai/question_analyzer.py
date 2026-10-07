import re

from src.metadata.semantic_registry import get_semantic_registry


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
    ],

    "On-Time Delivery Rate": [
        "on-time delivery rate",
        "on time delivery rate",
        "on-time delivery",
        "on time delivery",
        "delivery on time",
        "percentage of deliveries on time",
        "percent of deliveries on time",
        "on-time deliveries",
        "on time deliveries"
    ],

    "Repeat Customer Rate": [
        "repeat customer rate",
        "repeat customer",
        "repeat customers",
        "customer retention rate",
        "repeat buyer rate",
        "repeat buyers"
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

    if any(
        keyword in question_lower
        for keyword in [
            "why",
            "reason",
            "cause",
            "root cause",
            "driver"
        ]
    ):
        return "root_cause"

    if any(
        keyword in question_lower
        for keyword in [
            "compare",
            "comparison",
            "versus",
            "vs",
            "difference"
        ]
    ):
        return "comparison"

    if any(
        keyword in question_lower
        for keyword in [
            "top",
            "highest",
            "lowest",
            "best",
            "worst",
            "rank",
            "ranking"
        ]
    ):
        return "ranking"

    if any(
        keyword in question_lower
        for keyword in [
            "trend",
            "over time",
            "by month",
            "monthly",
            "by year",
            "yearly",
            "annually"
        ]
    ):
        return "trend_analysis"

    if any(
        keyword in question_lower
        for keyword in [
            "average",
            "mean",
            "median",
            "standard deviation",
            "variance",
            "distribution"
        ]
    ):
        return "statistical"

    if any(
        keyword in question_lower
        for keyword in [
            "how many",
            "count",
            "total",
            "sum",
            "what is",
            "what are"
        ]
    ):
        return "aggregation"

    return "unknown"


def detect_analysis_type(
    intent,
    metrics
):

    if (
        intent == "root_cause"
        and metrics
    ):
        return "metric_root_cause"

    if (
        intent == "comparison"
        and metrics
    ):
        return "metric_comparison"

    if (
        intent == "ranking"
        and metrics
    ):
        return "metric_ranking"

    if (
        intent == "trend_analysis"
        and metrics
    ):
        return "metric_trend"

    if (
        intent == "statistical"
        and metrics
    ):
        return "metric_statistics"

    if (
        intent == "aggregation"
        and metrics
    ):
        return "metric_aggregation"

    if intent == "root_cause":
        return "root_cause"

    if intent == "comparison":
        return "comparison"

    if intent == "ranking":
        return "ranking"

    if intent == "trend_analysis":
        return "trend"

    if intent == "statistical":
        return "statistics"

    if intent == "aggregation":
        return "aggregation"

    return "unknown"


def detect_metrics(
    question_lower
):

    semantic_registry = get_semantic_registry()

    detected_metrics = []

    for canonical_metric, patterns in METRIC_PATTERNS.items():

        if any(
            pattern in question_lower
            for pattern in patterns
        ):

            resolved_metric = (
                semantic_registry.resolve_metric(
                    candidate=canonical_metric
                )
            )

            if resolved_metric:

                detected_metrics.append(
                    resolved_metric
                )

    return detected_metrics


def detect_dimensions(
    question_lower,
    detected_metrics=None
):

    semantic_registry = get_semantic_registry()

    detected_metrics = detected_metrics or []

    # ---------------------------------------------------------
    # Remove metric phrases before detecting dimensions.
    #
    # Example:
    #
    # "What is the repeat customer rate?"
    #
    # The word "customer" belongs to the metric phrase and
    # should not independently create the Customer dimension.
    # ---------------------------------------------------------

    dimension_question = question_lower

    for metric in detected_metrics:

        patterns = METRIC_PATTERNS.get(
            metric,
            []
        )

        for pattern in patterns:

            dimension_question = (
                dimension_question.replace(
                    pattern,
                    " "
                )
            )

    detected_dimensions = []

    for canonical_dimension, patterns in DIMENSION_PATTERNS.items():

        if any(
            pattern in dimension_question
            for pattern in patterns
        ):

            resolved_dimension = (
                semantic_registry.resolve_dimension(
                    candidate=canonical_dimension
                )
            )

            if resolved_dimension:

                detected_dimensions.append(
                    resolved_dimension
                )

    return detected_dimensions


def detect_time_period(
    question
):

    years = re.findall(
        r"\b20\d{2}\b",
        question
    )

    if years:

        return years

    return None


def analyze_question(
    question
):

    question = question.strip()

    if not question:

        raise ValueError(
            "Question cannot be empty."
        )

    question_lower = question.lower()

    intent = detect_intent(
        question_lower
    )

    metrics = detect_metrics(
        question_lower
    )

    dimensions = detect_dimensions(
        question_lower,
        detected_metrics=metrics
    )

    analysis_type = detect_analysis_type(
        intent=intent,
        metrics=metrics
    )

    return {

        "original_question": question,

        "intent": intent,

        "analysis_type": analysis_type,

        "time_period": detect_time_period(
            question
        ),

        "metrics": metrics,

        "dimensions": dimensions,

        "filters": []

    }