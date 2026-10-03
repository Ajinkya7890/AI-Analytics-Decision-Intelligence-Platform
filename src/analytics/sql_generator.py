from src.analytics.analytical_planner import create_plan


def generate_sql(question):
    """
    Generate SQL from a structured analytical plan.

    This is the deterministic SQL generation layer.
    The LLM will be integrated later to improve
    natural-language understanding and planning.
    """

    plan = create_plan(question)

    intent = plan["intent"]
    metrics = plan["metrics"]
    dimensions = plan["dimensions"]
    time_period = plan["time_period"]
    source_tables = plan["source_tables"]

    if not source_tables:
        raise ValueError(
            "No analytical source table could be identified."
        )

    # --------------------------------------------------
    # Monthly Revenue Trend
    # --------------------------------------------------

    if (
        intent == "trend_analysis"
        and "Revenue" in metrics
        and "Month" in dimensions
    ):

        sql = """
SELECT
    DATE_TRUNC('month', full_date)::DATE AS month,
    SUM(revenue) AS revenue
FROM analytics.daily_sales
GROUP BY DATE_TRUNC('month', full_date)
ORDER BY month;
"""

        return sql.strip()

    # --------------------------------------------------
    # Product Revenue Ranking
    # --------------------------------------------------

    if (
        intent == "ranking"
        and "Revenue" in metrics
        and "Product" in dimensions
    ):

        sql = """
SELECT
    product_id,
    category_name_english,
    total_revenue
FROM analytics.product_metrics
ORDER BY total_revenue DESC
LIMIT 10;
"""

        return sql.strip()

    # --------------------------------------------------
    # Seller Revenue Ranking
    # --------------------------------------------------

    if (
        intent == "ranking"
        and "Revenue" in metrics
        and "Seller" in dimensions
    ):

        sql = """
SELECT
    seller_id,
    city,
    state,
    total_revenue
FROM analytics.seller_metrics
ORDER BY total_revenue DESC
LIMIT 10;
"""

        return sql.strip()

    # --------------------------------------------------
    # Average Delivery Time
    # --------------------------------------------------

    if (
        intent == "statistical"
        and "Average Delivery Days" in metrics
    ):

        sql = """
SELECT
    ROUND(AVG(delivery_days), 2) AS average_delivery_days
FROM analytics.delivery_metrics
WHERE delivery_days IS NOT NULL;
"""

        return sql.strip()

    # --------------------------------------------------
    # Revenue Root Cause - Initial baseline
    # --------------------------------------------------

    if (
        intent == "root_cause"
        and "Revenue" in metrics
    ):

        year_filter = ""

        if time_period:
            year = time_period[0]

            if year.isdigit():
                year_filter = f"""
WHERE EXTRACT(YEAR FROM full_date) = {int(year)}
"""

        sql = f"""
SELECT
    DATE_TRUNC('month', full_date)::DATE AS month,
    SUM(revenue) AS revenue
FROM analytics.daily_sales
{year_filter}
GROUP BY DATE_TRUNC('month', full_date)
ORDER BY month;
"""

        return sql.strip()

    raise ValueError(
        "No SQL generation rule is available for this analytical question."
    )