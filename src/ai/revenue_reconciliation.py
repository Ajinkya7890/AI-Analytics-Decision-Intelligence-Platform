from src.database.query_executor import execute_query


def reconcile_yearly_revenue(year):
    query = """
    SELECT
        %s AS year,

        (
            SELECT COALESCE(SUM(revenue), 0)
            FROM analytics.daily_sales
            WHERE EXTRACT(YEAR FROM full_date)::INTEGER = %s
        ) AS analytics_revenue,

        (
            SELECT COALESCE(SUM(oi.price), 0)
            FROM core.fact_order_item oi
            JOIN core.fact_order o
                ON oi.order_key = o.order_key
            WHERE EXTRACT(YEAR FROM o.purchase_timestamp)::INTEGER = %s
        ) AS core_revenue;
    """

    result = execute_query(
        query,
        (year, year, year)
    )

    row = result["rows"][0]

    return {
        "year": row[0],
        "analytics_revenue": float(row[1]),
        "core_revenue": float(row[2]),
        "difference": float(row[2]) - float(row[1])
    }


def print_reconciliation(years):
    print("REVENUE RECONCILIATION")
    print("=" * 80)

    for year in years:
        result = reconcile_yearly_revenue(year)

        print(f"\nYear: {result['year']}")
        print(
            f"  Analytics revenue: "
            f"₹{result['analytics_revenue']:,.2f}"
        )
        print(
            f"  Core revenue:      "
            f"₹{result['core_revenue']:,.2f}"
        )
        print(
            f"  Difference:        "
            f"₹{result['difference']:,.2f}"
        )