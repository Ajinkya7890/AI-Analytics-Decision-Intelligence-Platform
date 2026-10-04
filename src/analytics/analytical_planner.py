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


DIMENSION_GROUPING_MAP = {
    "Product": "product",
    "Seller": "seller",
    "Customer": "customer",
    "Month": "month",
    "Year": "year"
}


def select_source_tables(metrics, dimensions):
    """
    Select the most appropriate analytics table for
    each requested metric and dimension.
    """

    source_tables = []

    for metric in metrics:

        mapping = METRIC_TABLE_MAP.get(metric)

        if not mapping:
            continue

        selected_table = mapping.get("default")

        for dimension in dimensions:

            if dimension in mapping:
                selected_table = mapping[dimension]
                break

        if selected_table not in source_tables:
            source_tables.append(selected_table)

    return source_tables


def determine_operations(intent):
    """
    Map analytical intent to one or more analytical operations.
    """

    operation_map = {
        "trend_analysis": [
            "time_series_aggregation"
        ],

        "ranking": [
            "aggregation",
            "ranking"
        ],

        "comparison": [
            "group_comparison"
        ],

        "aggregation": [
            "aggregation"
        ],

        "statistical": [
            "statistical_summary"
        ],

        "root_cause": [
            "root_cause_analysis"
        ],

        "unknown": [
            "general_analysis"
        ]
    }

    return operation_map.get(
        intent,
        ["general_analysis"]
    )


def determine_group_by(dimensions):
    """
    Convert detected dimensions into generic grouping instructions.
    """

    group_by = []

    for dimension in dimensions:

        field = DIMENSION_GROUPING_MAP.get(
            dimension
        )

        if field and field not in group_by:
            group_by.append(field)

    return group_by


def determine_time_granularity(dimensions, intent):
    """
    Determine the requested time granularity.
    """

    if "Month" in dimensions:
        return "month"

    if "Year" in dimensions:
        return "year"

    if intent == "trend_analysis":
        return "time"

    return None


def determine_sorting(intent):
    """
    Determine default result ordering.
    """

    if intent == "ranking":
        return {
            "direction": "DESC",
            "limit": 10
        }

    if intent == "trend_analysis":
        return {
            "direction": "ASC",
            "limit": None
        }

    return None


def create_plan(question):
    """
    Convert a natural-language business question
    into a structured analytical plan.
    """

    analysis = analyze_question(question)

    metrics = analysis["metrics"]
    dimensions = analysis["dimensions"]
    intent = analysis["intent"]
    time_period = analysis["time_period"]
    filters = analysis["filters"]

    source_tables = select_source_tables(
        metrics=metrics,
        dimensions=dimensions
    )

    operations = determine_operations(
        intent=intent
    )

    group_by = determine_group_by(
        dimensions=dimensions
    )

    time_granularity = determine_time_granularity(
        dimensions=dimensions,
        intent=intent
    )

    sorting = determine_sorting(
        intent=intent
    )

    plan = {
        "question": question,
        "intent": intent,

        "metrics": metrics,
        "dimensions": dimensions,

        "time_period": time_period,
        "time_granularity": time_granularity,

        "filters": filters,

        "source_tables": source_tables,

        "operations": operations,

        "group_by": group_by,

        "sorting": sorting
    }

    return plan