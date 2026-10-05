from src.analytics.analytical_planner import create_plan
from src.metadata.metric_resolver import get_metric_resolver
from src.metadata.dimension_registry import get_dimension_registry


metric_resolver = get_metric_resolver()
dimension_registry = get_dimension_registry()


def get_metric_column(
    metric,
    source_table
):
    """
    Resolve the physical metric column from metadata.
    """

    metric_sources = metric_resolver.get_analytical_sources(
        metric
    )

    for source in metric_sources:

        if source["table_name"] == source_table:
            return source["column_name"]

    raise ValueError(
        f"No column mapping is available for metric "
        f"'{metric}' in table '{source_table}'."
    )


def get_dimension_columns(
    dimension,
    source_table
):
    """
    Resolve physical dimension columns from metadata.
    """

    sources = dimension_registry.get_sources(
        dimension
    )

    columns = []

    for source in sources:

        if source["table_name"] == source_table:

            columns.append(
                source["column_name"]
            )

    return columns


def source_supports_dimension(
    dimension,
    source_table
):
    """
    Check whether a source table supports a dimension.
    """

    return bool(
        get_dimension_columns(
            dimension,
            source_table
        )
    )


def source_supports_metric(
    metric,
    source_table
):
    """
    Check whether a source table supports a metric.
    """

    try:

        get_metric_column(
            metric,
            source_table
        )

        return True

    except ValueError:

        return False


def select_compatible_source_table(
    metric,
    dimensions,
    source_tables
):
    """
    Select a source table that supports both the metric
    and all requested dimensions.
    """

    for source_table in source_tables:

        if not source_supports_metric(
            metric,
            source_table
        ):
            continue

        if all(
            source_supports_dimension(
                dimension,
                source_table
            )
            for dimension in dimensions
        ):
            return source_table

    raise ValueError(
        f"No compatible analytical source table was found "
        f"for metric '{metric}' and dimensions {dimensions}."
    )


def get_metric_source_metadata(
    metric,
    source_table
):
    """
    Return complete metadata for a metric at a
    particular physical source.
    """

    source_metadata = (
        metric_resolver.get_source_metadata(
            metric,
            source_table
        )
    )

    if not source_metadata:

        raise ValueError(
            f"No source metadata is available for metric "
            f"'{metric}' in table '{source_table}'."
        )

    return source_metadata


def get_metric_aggregation_method(
    metric,
    source_table
):
    """
    Return the aggregation method registered for the
    selected metric source.
    """

    aggregation_method = (
        metric_resolver.get_aggregation_method(
            metric,
            source_table
        )
    )

    if not aggregation_method:

        raise ValueError(
            f"No aggregation method is registered for metric "
            f"'{metric}' in table '{source_table}'."
        )

    return aggregation_method.upper()


def get_metric_source_grain(
    metric,
    source_table
):
    """
    Return the source grain registered for a metric source.
    """

    return metric_resolver.get_source_grain(
        metric,
        source_table
    )


def get_metric_calculation_expression(
    metric,
    source_table
):
    """
    Return the calculation expression registered for
    a specific metric source.
    """

    return metric_resolver.get_calculation_expression(
        metric,
        source_table
    )


def get_metric_output_alias(
    metric,
    metric_column
):
    """
    Return a stable SQL output alias for a business metric.
    """

    alias_map = {
        "Revenue": "total_revenue",
        "Freight Revenue": "total_freight_revenue",
        "Total Order Value": "total_order_value",
        "Order Count": "total_orders",
        "Item Count": "total_items",
        "Average Order Value": "average_order_value",
        "Average Review Score": "average_review_score",
        "Average Delivery Days": "average_delivery_days",
        "On-Time Delivery Rate": "on_time_delivery_rate",
        "Repeat Customer Rate": "repeat_customer_rate"
    }

    return alias_map.get(
        metric,
        metric_column
    )


def get_dimension_expression(
    dimension,
    source_table
):
    """
    Convert a logical dimension into a SQL expression.
    """

    dimension_columns = get_dimension_columns(
        dimension,
        source_table
    )

    if not dimension_columns:

        raise ValueError(
            f"No column mapping is available for dimension "
            f"'{dimension}'."
        )

    column = dimension_columns[0]

    if dimension == "Month":

        return (
            f"DATE_TRUNC('month', {column})::DATE"
        )

    if dimension == "Year":

        return (
            f"DATE_TRUNC('year', {column})::DATE"
        )

    return column


def get_dimension_alias(
    dimension
):
    """
    Return a stable SQL alias for a logical dimension.
    """

    alias_map = {
        "Month": "month",
        "Year": "year",
        "Product": "product",
        "Seller": "seller",
        "Customer": "customer"
    }

    return alias_map.get(
        dimension,
        dimension.lower().replace(" ", "_")
    )


def build_metric_expression(
    metric,
    source_table
):
    """
    Build the SQL expression for a metric using
    source-level metadata.

    Supports:

        SUM(...)
        AVG(...)
        MIN(...)
        MAX(...)
        COUNT(...)
        DIRECT
        derived calculation expressions
    """

    metric_column = get_metric_column(
        metric,
        source_table
    )

    source_metadata = get_metric_source_metadata(
        metric,
        source_table
    )

    aggregation_method = (
        get_metric_aggregation_method(
            metric,
            source_table
        )
    )

    calculation_expression = (
        source_metadata.get(
            "calculation_expression"
        )
    )

    metric_definition = metric_resolver.get_metric(
        metric
    )

    metric_type = (
        metric_definition.get("metric_type")
        if metric_definition
        else None
    )

    # ---------------------------------------------------------
    # Derived metrics
    # ---------------------------------------------------------

    if (
        metric_type == "derived_ratio"
        and calculation_expression
    ):

        return calculation_expression

    # ---------------------------------------------------------
    # Direct analytical metric
    # ---------------------------------------------------------

    if aggregation_method == "DIRECT":

        return metric_column

    # ---------------------------------------------------------
    # Standard aggregations
    # ---------------------------------------------------------

    supported_aggregations = {
        "SUM",
        "AVG",
        "MIN",
        "MAX",
        "COUNT"
    }

    if aggregation_method not in supported_aggregations:

        raise ValueError(
            f"Unsupported aggregation method "
            f"'{aggregation_method}' for metric "
            f"'{metric}'."
        )

    return (
        f"{aggregation_method}"
        f"({metric_column})"
    )


def generate_generic_aggregation_sql(
    plan
):
    """
    Generate generic metadata-driven analytical SQL.

    Supports:

        metric
        metric + dimension
        metric + multiple dimensions

    Aggregation behavior and derived calculations
    come from metadata.metric_sources.
    """

    metrics = plan.get(
        "metrics",
        []
    )

    dimensions = plan.get(
        "dimensions",
        []
    )

    source_tables = plan.get(
        "source_tables",
        []
    )

    if not metrics:

        raise ValueError(
            "No metric was identified for aggregation."
        )

    if not source_tables:

        raise ValueError(
            "No analytical source table was identified."
        )

    metric = metrics[0]

    source_table = select_compatible_source_table(
        metric=metric,
        dimensions=dimensions,
        source_tables=source_tables
    )

    metric_column = get_metric_column(
        metric,
        source_table
    )

    metric_alias = get_metric_output_alias(
        metric,
        metric_column
    )

    metric_expression = build_metric_expression(
        metric,
        source_table
    )

    aggregation_method = (
        get_metric_aggregation_method(
            metric,
            source_table
        )
    )

    metric_definition = metric_resolver.get_metric(
        metric
    )

    metric_type = (
        metric_definition.get("metric_type")
        if metric_definition
        else None
    )

    # ---------------------------------------------------------
    # No dimensions
    # ---------------------------------------------------------

    if not dimensions:

        return f"""
SELECT
    {metric_expression} AS {metric_alias}
FROM {source_table};
""".strip()

    select_parts = []

    group_by_parts = []

    for dimension in dimensions:

        expression = get_dimension_expression(
            dimension,
            source_table
        )

        alias = get_dimension_alias(
            dimension
        )

        select_parts.append(
            f"{expression} AS {alias}"
        )

        group_by_parts.append(
            expression
        )

    select_clause = ",\n    ".join(
        select_parts
    )

    group_by_clause = ", ".join(
        group_by_parts
    )

    # ---------------------------------------------------------
    # Derived ratio metrics
    #
    # A derived metric contains its own aggregation logic.
    # However, when dimensions are present, the calculation
    # must be evaluated separately for every dimension group.
    # ---------------------------------------------------------

    if metric_type == "derived_ratio":

        # Time dimensions should be chronological.
        if "Month" in dimensions:

            return f"""
SELECT
    {select_clause},
    {metric_expression} AS {metric_alias}
FROM {source_table}
GROUP BY {group_by_clause}
ORDER BY month;
""".strip()

        if "Year" in dimensions:

            return f"""
SELECT
    {select_clause},
    {metric_expression} AS {metric_alias}
FROM {source_table}
GROUP BY {group_by_clause}
ORDER BY year;
""".strip()

        return f"""
SELECT
    {select_clause},
    {metric_expression} AS {metric_alias}
FROM {source_table}
GROUP BY {group_by_clause}
ORDER BY {metric_alias} DESC;
""".strip()

    # ---------------------------------------------------------
    # Direct analytical metrics
    # ---------------------------------------------------------

    if aggregation_method == "DIRECT":

        return f"""
SELECT
    {select_clause},
    {metric_expression} AS {metric_alias}
FROM {source_table}
ORDER BY {metric_alias} DESC;
""".strip()

    # ---------------------------------------------------------
    # Time dimensions for standard aggregated metrics
    # ---------------------------------------------------------

    if "Month" in dimensions:

        return f"""
SELECT
    {select_clause},
    {metric_expression} AS {metric_alias}
FROM {source_table}
GROUP BY {group_by_clause}
ORDER BY month;
""".strip()

    if "Year" in dimensions:

        return f"""
SELECT
    {select_clause},
    {metric_expression} AS {metric_alias}
FROM {source_table}
GROUP BY {group_by_clause}
ORDER BY year;
""".strip()

    # ---------------------------------------------------------
    # Standard aggregated metrics
    # ---------------------------------------------------------

    return f"""
SELECT
    {select_clause},
    {metric_expression} AS {metric_alias}
FROM {source_table}
GROUP BY {group_by_clause}
ORDER BY {metric_alias} DESC;
""".strip()


def generate_monthly_revenue_sql(
    plan
):
    """
    Generate monthly revenue trend SQL.
    """

    metric = "Revenue"

    source_table = select_compatible_source_table(
        metric=metric,
        dimensions=["Month"],
        source_tables=plan.get(
            "source_tables",
            []
        )
    )

    metric_column = get_metric_column(
        metric,
        source_table
    )

    month_columns = get_dimension_columns(
        "Month",
        source_table
    )

    if not month_columns:

        raise ValueError(
            "No date column is available for the Month dimension."
        )

    date_column = month_columns[0]

    return f"""
SELECT
    DATE_TRUNC('month', {date_column})::DATE AS month,
    SUM({metric_column}) AS revenue
FROM {source_table}
GROUP BY DATE_TRUNC('month', {date_column})
ORDER BY month;
""".strip()


def generate_product_revenue_ranking_sql(
    plan
):
    """
    Generate top-product revenue ranking SQL.
    """

    metric = "Revenue"
    dimension = "Product"

    sorting = plan.get(
        "sorting"
    ) or {}

    direction = sorting.get(
        "direction",
        "DESC"
    )

    limit = sorting.get(
        "limit",
        10
    )

    source_table = select_compatible_source_table(
        metric=metric,
        dimensions=[dimension],
        source_tables=plan.get(
            "source_tables",
            []
        )
    )

    metric_column = get_metric_column(
        metric,
        source_table
    )

    dimension_columns = get_dimension_columns(
        dimension,
        source_table
    )

    if not dimension_columns:

        raise ValueError(
            "No Product dimension columns are available."
        )

    select_columns = list(
        dict.fromkeys(
            dimension_columns
        )
    )

    select_clause = ",\n    ".join(
        select_columns
    )

    return f"""
SELECT
    {select_clause},
    {metric_column} AS total_revenue
FROM {source_table}
ORDER BY total_revenue {direction}
LIMIT {limit};
""".strip()


def generate_seller_revenue_ranking_sql(
    plan
):
    """
    Generate top-seller revenue ranking SQL.
    """

    metric = "Revenue"
    dimension = "Seller"

    sorting = plan.get(
        "sorting"
    ) or {}

    direction = sorting.get(
        "direction",
        "DESC"
    )

    limit = sorting.get(
        "limit",
        10
    )

    source_table = select_compatible_source_table(
        metric=metric,
        dimensions=[dimension],
        source_tables=plan.get(
            "source_tables",
            []
        )
    )

    metric_column = get_metric_column(
        metric,
        source_table
    )

    dimension_columns = get_dimension_columns(
        dimension,
        source_table
    )

    if not dimension_columns:

        raise ValueError(
            "No Seller dimension columns are available."
        )

    select_columns = list(
        dict.fromkeys(
            dimension_columns
        )
    )

    select_clause = ",\n    ".join(
        select_columns
    )

    return f"""
SELECT
    {select_clause},
    {metric_column} AS total_revenue
FROM {source_table}
ORDER BY total_revenue {direction}
LIMIT {limit};
""".strip()


def generate_average_delivery_sql(
    plan
):
    """
    Generate average delivery time SQL.
    """

    metric = "Average Delivery Days"

    source_table = select_compatible_source_table(
        metric=metric,
        dimensions=[],
        source_tables=plan.get(
            "source_tables",
            []
        )
    )

    metric_column = get_metric_column(
        metric,
        source_table
    )

    return f"""
SELECT
    ROUND(AVG({metric_column}), 2) AS average_delivery_days
FROM {source_table}
WHERE {metric_column} IS NOT NULL;
""".strip()


def generate_statistical_sql(
    plan
):
    """
    Generate raw metric SQL for statistical analysis.

    This function is used only when there are no dimensions
    and the metric is genuinely intended for statistical
    analysis.
    """

    metrics = plan.get(
        "metrics",
        []
    )

    source_tables = plan.get(
        "source_tables",
        []
    )

    if not metrics:

        raise ValueError(
            "No metric was identified for statistical analysis."
        )

    if not source_tables:

        raise ValueError(
            "No source table was identified for statistical analysis."
        )

    metric = metrics[0]

    source_table = select_compatible_source_table(
        metric=metric,
        dimensions=[],
        source_tables=source_tables
    )

    metric_column = get_metric_column(
        metric,
        source_table
    )

    return f"""
SELECT
    {metric_column}
FROM {source_table}
WHERE {metric_column} IS NOT NULL;
""".strip()


def generate_root_cause_baseline_sql(
    plan
):
    """
    Generate the baseline monthly revenue series used
    by the root-cause analysis pipeline.
    """

    metric = "Revenue"

    source_table = select_compatible_source_table(
        metric=metric,
        dimensions=["Month"],
        source_tables=plan.get(
            "source_tables",
            []
        )
    )

    metric_column = get_metric_column(
        metric,
        source_table
    )

    month_columns = get_dimension_columns(
        "Month",
        source_table
    )

    if not month_columns:

        raise ValueError(
            "No date column is available for the Month dimension."
        )

    date_column = month_columns[0]

    time_period = plan.get(
        "time_period"
    )

    year_filter = ""

    if time_period:

        year = time_period[0]

        if year.isdigit():

            year_filter = f"""
WHERE EXTRACT(YEAR FROM {date_column}) = {int(year)}
"""

    return f"""
SELECT
    DATE_TRUNC('month', {date_column})::DATE AS month,
    SUM({metric_column}) AS revenue
FROM {source_table}
{year_filter}
GROUP BY DATE_TRUNC('month', {date_column})
ORDER BY month;
""".strip()


def generate_seller_revenue_comparison_sql(
    plan
):
    """
    Generate seller revenue comparison SQL.
    """

    metric = "Revenue"
    dimension = "Seller"

    source_table = select_compatible_source_table(
        metric=metric,
        dimensions=[dimension],
        source_tables=plan.get(
            "source_tables",
            []
        )
    )

    metric_column = get_metric_column(
        metric,
        source_table
    )

    dimension_columns = get_dimension_columns(
        dimension,
        source_table
    )

    if not dimension_columns:

        raise ValueError(
            "No Seller dimension columns are available."
        )

    select_columns = list(
        dict.fromkeys(
            dimension_columns
        )
    )

    select_clause = ",\n    ".join(
        select_columns
    )

    return f"""
SELECT
    {select_clause},
    {metric_column} AS total_revenue
FROM {source_table}
ORDER BY total_revenue DESC
LIMIT 10;
""".strip()


def generate_sql(
    question
):
    """
    Generate SQL from a natural-language analytical question.

    The analytical plan is created first, followed by
    metadata-driven source resolution and SQL generation.
    """

    plan = create_plan(
        question
    )

    intent = plan["intent"]
    metrics = plan["metrics"]
    dimensions = plan["dimensions"]
    source_tables = plan["source_tables"]

    if not source_tables:

        raise ValueError(
            "No analytical source table could be identified."
        )

    # ---------------------------------------------------------
    # Specialized analytical strategies
    # ---------------------------------------------------------

    if (
        intent == "trend_analysis"
        and "Revenue" in metrics
        and "Month" in dimensions
    ):

        return generate_monthly_revenue_sql(
            plan
        )

    if (
        intent == "ranking"
        and "Revenue" in metrics
        and "Product" in dimensions
    ):

        return generate_product_revenue_ranking_sql(
            plan
        )

    if (
        intent == "ranking"
        and "Revenue" in metrics
        and "Seller" in dimensions
    ):

        return generate_seller_revenue_ranking_sql(
            plan
        )

    if (
        intent == "comparison"
        and "Revenue" in metrics
        and "Seller" in dimensions
    ):

        return generate_seller_revenue_comparison_sql(
            plan
        )

    if (
        intent == "root_cause"
        and "Revenue" in metrics
    ):

        return generate_root_cause_baseline_sql(
            plan
        )

    # ---------------------------------------------------------
    # Average delivery specialized metric
    #
    # This must come before the generic statistical branch
    # because delivery-time questions may be classified as
    # statistical by the question analyzer.
    # ---------------------------------------------------------

    if (
        "Average Delivery Days" in metrics
        and not dimensions
    ):

        return generate_average_delivery_sql(
            plan
        )

    # ---------------------------------------------------------
    # Derived metrics
    #
    # Derived metrics must be routed through the generic
    # metadata-driven generator before the statistical branch.
    # ---------------------------------------------------------

    if (
        "Average Order Value" in metrics
    ):

        return generate_generic_aggregation_sql(
            plan
        )

    # ---------------------------------------------------------
    # Statistical analysis without dimensions
    # ---------------------------------------------------------

    if (
        intent == "statistical"
        and not dimensions
    ):

        return generate_statistical_sql(
            plan
        )

    # ---------------------------------------------------------
    # Generic metadata-driven aggregation
    # ---------------------------------------------------------

    if metrics:

        return generate_generic_aggregation_sql(
            plan
        )

    raise ValueError(
        "No SQL generation rule is available for "
        "this analytical question."
    )