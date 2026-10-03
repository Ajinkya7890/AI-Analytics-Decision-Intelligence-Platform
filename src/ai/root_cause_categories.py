from src.database.query_executor import execute_query


def compare_category_revenue(current_year, previous_year):
    query = """
    SELECT
        COALESCE(p.category_name_english, 'unknown') AS category,

        SUM(
            CASE
                WHEN EXTRACT(YEAR FROM o.purchase_timestamp)::INTEGER = %s
                THEN oi.price
                ELSE 0
            END
        ) AS previous_revenue,

        SUM(
            CASE
                WHEN EXTRACT(YEAR FROM o.purchase_timestamp)::INTEGER = %s
                THEN oi.price
                ELSE 0
            END
        ) AS current_revenue,

        SUM(
            CASE
                WHEN EXTRACT(YEAR FROM o.purchase_timestamp)::INTEGER = %s
                THEN oi.price
                ELSE 0
            END
        )
        -
        SUM(
            CASE
                WHEN EXTRACT(YEAR FROM o.purchase_timestamp)::INTEGER = %s
                THEN oi.price
                ELSE 0
            END
        ) AS revenue_change

    FROM core.fact_order_item oi

    JOIN core.fact_order o
        ON oi.order_key = o.order_key

    JOIN core.dim_product p
        ON oi.product_key = p.product_key

    WHERE EXTRACT(YEAR FROM o.purchase_timestamp)::INTEGER
          IN (%s, %s)

    GROUP BY
        COALESCE(p.category_name_english, 'unknown')

    ORDER BY revenue_change DESC;
    """

    result = execute_query(
        query,
        (
            previous_year,
            current_year,
            current_year,
            previous_year,
            previous_year,
            current_year
        )
    )

    return result


def print_category_contributors(current_year, previous_year):
    result = compare_category_revenue(
        current_year,
        previous_year
    )

    print("CATEGORY REVENUE CONTRIBUTORS")
    print("=" * 100)

    for row in result["rows"]:
        print(
            f"Category: {row[0]} | "
            f"Previous: ₹{row[1]:,.2f} | "
            f"Current: ₹{row[2]:,.2f} | "
            f"Change: ₹{row[3]:,.2f}"
        )