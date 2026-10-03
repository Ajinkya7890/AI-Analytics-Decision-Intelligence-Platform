from src.ai.question_analyzer import analyze_question


METRIC_TABLE_MAP = {
    "Revenue": {
        "default": "analytics.daily_sales",
        "Product": "analytics.product_metrics",
        "Seller": "analytics.seller_metrics",
        "Customer": "analytics.customer_metrics"
    },

    "Freight Revenue": {
        "default": "analytics.daily_sales",
        "Product": "analytics.product_metrics",
        "Seller": "analytics.seller_metrics",
        "Customer": "analytics.customer_metrics"
    },

    "Total Order Value": {
        "default": "analytics.daily_sales",
        "Product": "analytics.product_metrics",
        "Seller": "analytics.seller_metrics",
        "Customer": "analytics.customer_metrics"
    },

    "Order Count": {
        "default": "analytics.daily_sales",
        "Product": "analytics.product_metrics",
        "Seller": "analytics.seller_metrics",
        "Customer": "analytics.customer_metrics"
    },

    "Item Count": {
        "default": "analytics.daily_sales",
        "Product": "analytics.product_metrics",
        "Seller": "analytics.seller_metrics"
    },

    "Average Order Value": {
        "default": "analytics.daily_sales",
        "Customer": "analytics.customer_metrics"
    },

    "Average Review Score": {
        "default": "analytics.review_metrics"
    },

    "Average Delivery Days": {
        "default": "analytics.delivery_metrics"
    }
}


def create_plan(question):
    """
    Convert a natural-language business question
    into a structured analytical plan.
    """

    analysis = analyze_question(question)

    metrics = analysis["metrics"]
    dimensions = analysis["dimensions"]
    intent = analysis["intent"]

    plan = {
        "question": question,
        "intent": intent,
        "metrics": metrics,
        "dimensions": dimensions,
        "time_period": analysis["time_period"],
        "filters": analysis["filters"],
        "source_tables": [],
        "operations": []
    }

    # --------------------------------------------------
    # Identify source tables based on metric + dimension
    # --------------------------------------------------

    for metric in metrics:

        mapping = METRIC_TABLE_MAP.get(metric)

        if not mapping:
            continue

        selected_table = mapping.get("default")

        # Prefer a dimension-specific analytical table
        for dimension in dimensions:

            if dimension in mapping:
                selected_table = mapping[dimension]
                break

        if selected_table not in plan["source_tables"]:
            plan["source_tables"].append(selected_table)

    # --------------------------------------------------
    # Determine analytical operation
    # --------------------------------------------------

    if intent == "trend_analysis":

        plan["operations"].append(
            "time_series_aggregation"
        )

    elif intent == "ranking":

        plan["operations"].append(
            "ranking"
        )

    elif intent == "comparison":

        plan["operations"].append(
            "group_comparison"
        )

    elif intent == "aggregation":

        plan["operations"].append(
            "aggregation"
        )

    elif intent == "statistical":

        plan["operations"].append(
            "statistical_summary"
        )

    elif intent == "root_cause":

        plan["operations"].append(
            "root_cause_analysis"
        )

    else:

        plan["operations"].append(
            "general_analysis"
        )

    return plan