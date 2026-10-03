from src.database.query_executor import execute_query
from src.statistics.analyzer import percentage_change


def get_yearly_revenue():
    """
    Retrieve yearly revenue from the analytics layer.
    """

    query = """
    SELECT
        EXTRACT(YEAR FROM full_date)::INTEGER AS year,
        SUM(revenue) AS revenue
    FROM analytics.daily_sales
    GROUP BY EXTRACT(YEAR FROM full_date)
    ORDER BY year;
    """

    result = execute_query(query)

    return result["rows"]


def compare_years(current_year, previous_year):
    """
    Compare revenue between two years.
    """

    yearly_data = get_yearly_revenue()

    revenue_by_year = {
        row[0]: float(row[1])
        for row in yearly_data
    }

    current_revenue = revenue_by_year.get(current_year)
    previous_revenue = revenue_by_year.get(previous_year)

    if current_revenue is None:
        raise ValueError(
            f"No revenue data found for {current_year}."
        )

    if previous_revenue is None:
        raise ValueError(
            f"No revenue data found for {previous_year}."
        )

    change = percentage_change(
        previous_revenue,
        current_revenue
    )

    return {
        "previous_year": previous_year,
        "current_year": current_year,
        "previous_revenue": previous_revenue,
        "current_revenue": current_revenue,
        "percentage_change": change
    }