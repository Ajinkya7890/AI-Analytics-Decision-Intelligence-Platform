from src.analytics.analytical_planner import create_plan
from src.analytics.sql_generator import generate_sql
from src.database.sql_validator import validate_sql
from src.database.query_executor import execute_query
from src.statistics.analyzer import descriptive_statistics


# Maps analytical metrics to the result columns that contain
# the corresponding numeric values.
METRIC_RESULT_COLUMNS = {
    "Revenue": [
        "revenue",
        "total_revenue",
        "total_spend",
    ],
    "Freight Revenue": [
        "freight_revenue",
        "total_freight",
        "total_freight_revenue",
    ],
    "Order Count": [
        "order_count",
        "total_orders",
    ],
    "Item Count": [
        "item_count",
        "total_items",
    ],
    "Average Order Value": [
        "aov",
        "average_order_value",
    ],
    "Average Review Score": [
        "average_review_score",
    ],
    "Average Delivery Days": [
        "delivery_days",
        "average_delivery_days",
    ],
}


def extract_metric_values(metric, columns, rows):
    """
    Extract only the numeric result column associated
    with the requested analytical metric.
    """

    possible_columns = METRIC_RESULT_COLUMNS.get(
        metric,
        []
    )

    metric_column_index = None

    for index, column in enumerate(columns):
        if column in possible_columns:
            metric_column_index = index
            break

    if metric_column_index is None:
        return []

    values = []

    for row in rows:
        value = row[metric_column_index]

        if value is not None:
            values.append(value)

    return values


def run_question(question):
    """
    Complete analytical query pipeline.

    Question
        ↓
    Analytical Plan
        ↓
    SQL Generation
        ↓
    SQL Validation
        ↓
    SQL Execution
        ↓
    Metric-aware Statistical Analysis
        ↓
    Results
    """

    # --------------------------------------------------
    # Step 1 — Create analytical plan
    # --------------------------------------------------

    plan = create_plan(question)

    # --------------------------------------------------
    # Step 2 — Generate SQL
    # --------------------------------------------------

    sql = generate_sql(question)

    # --------------------------------------------------
    # Step 3 — Validate SQL
    # --------------------------------------------------

    is_valid, validation_message = validate_sql(sql)

    if not is_valid:
        raise ValueError(
            f"Generated SQL failed validation: "
            f"{validation_message}"
        )

    # --------------------------------------------------
    # Step 4 — Execute SQL
    # --------------------------------------------------

    result = execute_query(sql)

    columns = result["columns"]
    rows = result["rows"]

    # --------------------------------------------------
    # Step 5 — Metric-aware statistical analysis
    # --------------------------------------------------

    statistics = None

    if plan["intent"] == "statistical":

        metrics = plan.get("metrics", [])

        if metrics:
            metric = metrics[0]

            metric_values = extract_metric_values(
                metric=metric,
                columns=columns,
                rows=rows
            )

            if metric_values:
                statistics = descriptive_statistics(
                    *metric_values
                )

    # --------------------------------------------------
    # Step 6 — Return everything needed downstream
    # --------------------------------------------------

    return {
        "question": question,
        "plan": plan,
        "sql": sql,
        "validation": validation_message,
        "columns": columns,
        "rows": rows,
        "statistics": statistics
    }