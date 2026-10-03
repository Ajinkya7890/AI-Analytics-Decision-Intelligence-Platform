from src.database.query_executor import execute_query


def compare_product_revenue(current_year, previous_year):
    query = """
    SELECT
        p.product_id,
        p.category_name_english,

        COALESCE(
            SUM(
                CASE
                    WHEN EXTRACT(YEAR FROM o.purchase_timestamp)::INTEGER = %s
                    THEN oi.price
                    ELSE 0
                END
            ),
            0
        ) AS previous_revenue,

        COALESCE(
            SUM(
                CASE
                    WHEN EXTRACT(YEAR FROM o.purchase_timestamp)::INTEGER = %s
                    THEN oi.price
                    ELSE 0
                END
            ),
            0
        ) AS current_revenue,

        COALESCE(
            SUM(
                CASE
                    WHEN EXTRACT(YEAR FROM o.purchase_timestamp)::INTEGER = %s
                    THEN oi.price
                    ELSE 0
                END
            ),
            0
        )
        -
        COALESCE(
            SUM(
                CASE
                    WHEN EXTRACT(YEAR FROM o.purchase_timestamp)::INTEGER = %s
                    THEN oi.price
                    ELSE 0
                END
            ),
            0
        ) AS revenue_change

    FROM core.fact_order_item oi

    JOIN core.fact_order o
        ON oi.order_key = o.order_key

    JOIN core.dim_product p
        ON oi.product_key = p.product_key

    WHERE EXTRACT(YEAR FROM o.purchase_timestamp)::INTEGER
          IN (%s, %s)

    GROUP BY
        p.product_id,
        p.category_name_english

    ORDER BY revenue_change DESC

    LIMIT 10;
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


def print_product_contributors(current_year, previous_year):
    result = compare_product_revenue(
        current_year,
        previous_year
    )

    print("TOP PRODUCT REVENUE CONTRIBUTORS")
    print("=" * 80)

    for row in result["rows"]:
        print(
            f"Product: {row[0]} | "
            f"Category: {row[1]} | "
            f"Previous: {row[2]:,.2f} | "
            f"Current: {row[3]:,.2f} | "
            f"Change: {row[4]:,.2f}"
        )