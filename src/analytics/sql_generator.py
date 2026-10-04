from src.analytics.analytical_planner import create_plan


METRIC_COLUMN_MAP = {
    "Revenue": {
        "analytics.daily_sales": "revenue",
        "analytics.product_metrics": "total_revenue",
        "analytics.seller_metrics": "total_revenue",
        "analytics.customer_metrics": "total_spend",
    },
    "Freight Revenue": {
        "analytics.daily_sales": "freight_revenue",
        "analytics.product_metrics": "total_freight",
        "analytics.seller_metrics": "total_freight",
        "analytics.customer_metrics": "total_freight",
    },
    "Order Count": {
        "analytics.daily_sales": "order_count",
        "analytics.product_metrics": "total_orders",
        "analytics.seller_metrics": "total_orders",
        "analytics.customer_metrics": "total_orders",
    },
    "Item Count": {
        "analytics.daily_sales": "item_count",
        "analytics.product_metrics": "total_items",
        "analytics.seller_metrics": "total_items",
    },
    "Average Order Value": {
        "analytics.daily_sales": "aov",
        "analytics.customer_metrics": "average_order_value",
    },
    "Average Review Score": {
        "analytics.review_metrics": "average_review_score",
    },
    "Average Delivery Days": {
        "analytics.delivery_metrics": "delivery_days",
    },
}


DIMENSION_COLUMNS = {
    "Product": {
        "analytics.product_metrics": [
            "product_id",
            "category_name_english",
        ]
    },
    "Seller": {
        "analytics.seller_metrics": [
            "seller_id",
            "city",
            "state",
        ]
    },
    "Customer": {
        "analytics.customer_metrics": [
            "customer_unique_id",
        ]
    },
}


def generate_monthly_revenue_sql(plan):
    return """
SELECT
    DATE_TRUNC('month', full_date)::DATE AS month,
    SUM(revenue) AS revenue
FROM analytics.daily_sales
GROUP BY DATE_TRUNC('month', full_date)
ORDER BY month;
""".strip()


def generate_product_revenue_ranking_sql(plan):
    sorting = plan.get("sorting") or {}

    direction = sorting.get("direction", "DESC")
    limit = sorting.get("limit", 10)

    return f"""
SELECT
    product_id,
    category_name_english,
    total_revenue
FROM analytics.product_metrics
ORDER BY total_revenue {direction}
LIMIT {limit};
""".strip()


def generate_seller_revenue_ranking_sql(plan):
    sorting = plan.get("sorting") or {}

    direction = sorting.get("direction", "DESC")
    limit = sorting.get("limit", 10)

    return f"""
SELECT
    seller_id,
    city,
    state,
    total_revenue
FROM analytics.seller_metrics
ORDER BY total_revenue {direction}
LIMIT {limit};
""".strip()


def generate_average_delivery_sql(plan):
    return """
SELECT
    ROUND(AVG(delivery_days), 2) AS average_delivery_days
FROM analytics.delivery_metrics
WHERE delivery_days IS NOT NULL;
""".strip()


def generate_statistical_sql(plan):
    """
    Generate SQL for statistical analysis of a metric.
    """

    metrics = plan.get("metrics", [])
    source_tables = plan.get("source_tables", [])

    if not metrics:
        raise ValueError(
            "No metric was identified for statistical analysis."
        )

    if not source_tables:
        raise ValueError(
            "No source table was identified for statistical analysis."
        )

    metric = metrics[0]
    source_table = source_tables[0]

    metric_mapping = METRIC_COLUMN_MAP.get(metric)

    if not metric_mapping:
        raise ValueError(
            f"No metric mapping is available for '{metric}'."
        )

    metric_column = metric_mapping.get(source_table)

    if not metric_column:
        raise ValueError(
            f"No column mapping is available for metric "
            f"'{metric}' in table '{source_table}'."
        )

    return f"""
SELECT
    {metric_column}
FROM {source_table}
WHERE {metric_column} IS NOT NULL;
""".strip()


def generate_root_cause_baseline_sql(plan):
    time_period = plan.get("time_period")
    year_filter = ""

    if time_period:
        year = time_period[0]

        if year.isdigit():
            year_filter = f"""
WHERE EXTRACT(YEAR FROM full_date) = {int(year)}
"""

    return f"""
SELECT
    DATE_TRUNC('month', full_date)::DATE AS month,
    SUM(revenue) AS revenue
FROM analytics.daily_sales
{year_filter}
GROUP BY DATE_TRUNC('month', full_date)
ORDER BY month;
""".strip()


def generate_seller_revenue_comparison_sql(plan):
    return """
SELECT
    seller_id,
    city,
    state,
    total_revenue
FROM analytics.seller_metrics
ORDER BY total_revenue DESC
LIMIT 10;
""".strip()


def generate_aggregation_sql(plan):
    metrics = plan.get("metrics", [])
    dimensions = plan.get("dimensions", [])
    source_tables = plan.get("source_tables", [])

    if not metrics:
        raise ValueError(
            "No metric was identified for aggregation."
        )

    if not source_tables:
        raise ValueError(
            "No source table was identified for aggregation."
        )

    metric = metrics[0]
    source_table = source_tables[0]

    metric_mapping = METRIC_COLUMN_MAP.get(metric)

    if not metric_mapping:
        raise ValueError(
            f"No metric mapping is available for '{metric}'."
        )

    metric_column = metric_mapping.get(source_table)

    if not metric_column:
        raise ValueError(
            f"No column mapping is available for metric "
            f"'{metric}' in table '{source_table}'."
        )

    # ---------------------------------------------------------
    # Determine output alias from the actual metric column
    # ---------------------------------------------------------

    alias_map = {
        "revenue": "total_revenue",
        "total_revenue": "total_revenue",
        "total_spend": "total_spend",
        "freight_revenue": "total_freight_revenue",
        "total_freight": "total_freight",
        "order_count": "total_orders",
        "total_orders": "total_orders",
        "item_count": "total_items",
        "total_items": "total_items",
        "aov": "average_order_value",
        "average_order_value": "average_order_value",
        "average_review_score": "average_review_score",
        "delivery_days": "average_delivery_days",
    }

    metric_alias = alias_map.get(
        metric_column,
        metric_column
    )

    # ---------------------------------------------------------
    # Scalar aggregation
    # ---------------------------------------------------------

    if not dimensions:
        return f"""
SELECT
    SUM({metric_column}) AS {metric_alias}
FROM {source_table};
""".strip()

    # ---------------------------------------------------------
    # Dimension-based aggregation
    # ---------------------------------------------------------

    select_columns = []

    for dimension in dimensions:

        dimension_mapping = DIMENSION_COLUMNS.get(dimension)

        if not dimension_mapping:
            raise ValueError(
                f"No dimension mapping is available for '{dimension}'."
            )

        dimension_columns = dimension_mapping.get(source_table)

        if not dimension_columns:
            raise ValueError(
                f"No column mapping is available for dimension "
                f"'{dimension}' in table '{source_table}'."
            )

        select_columns.extend(dimension_columns)

    # Remove duplicate columns while preserving order
    select_columns = list(dict.fromkeys(select_columns))

    select_clause = ",\n    ".join(select_columns)

    group_by_clause = ", ".join(select_columns)

    return f"""
SELECT
    {select_clause},
    SUM({metric_column}) AS {metric_alias}
FROM {source_table}
GROUP BY {group_by_clause}
ORDER BY {metric_alias} DESC;
""".strip()


def generate_sql(question):
    plan = create_plan(question)

    intent = plan["intent"]
    metrics = plan["metrics"]
    dimensions = plan["dimensions"]
    source_tables = plan["source_tables"]

    if not source_tables:
        raise ValueError(
            "No analytical source table could be identified."
        )

    # ---------------------------------------------------------
    # Trend analysis
    # ---------------------------------------------------------

    if (
        intent == "trend_analysis"
        and "Revenue" in metrics
        and "Month" in dimensions
    ):
        return generate_monthly_revenue_sql(plan)

    # ---------------------------------------------------------
    # Product ranking
    # ---------------------------------------------------------

    if (
        intent == "ranking"
        and "Revenue" in metrics
        and "Product" in dimensions
    ):
        return generate_product_revenue_ranking_sql(plan)

    # ---------------------------------------------------------
    # Seller ranking
    # ---------------------------------------------------------

    if (
        intent == "ranking"
        and "Revenue" in metrics
        and "Seller" in dimensions
    ):
        return generate_seller_revenue_ranking_sql(plan)

    # ---------------------------------------------------------
    # Statistical analysis
    # ---------------------------------------------------------

    if intent == "statistical":
        return generate_statistical_sql(plan)

    # ---------------------------------------------------------
    # Seller comparison
    # ---------------------------------------------------------

    if (
        intent == "comparison"
        and "Revenue" in metrics
        and "Seller" in dimensions
    ):
        return generate_seller_revenue_comparison_sql(plan)

    # ---------------------------------------------------------
    # Generic aggregation
    # ---------------------------------------------------------

    if intent == "aggregation":
        return generate_aggregation_sql(plan)

    # ---------------------------------------------------------
    # Revenue root cause
    # ---------------------------------------------------------

    if (
        intent == "root_cause"
        and "Revenue" in metrics
    ):
        return generate_root_cause_baseline_sql(plan)

    raise ValueError(
        "No SQL generation rule is available for this analytical question."
    )