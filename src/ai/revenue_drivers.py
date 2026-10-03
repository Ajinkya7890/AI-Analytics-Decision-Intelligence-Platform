from src.database.query_executor import execute_query


def analyze_category_drivers(current_year, previous_year):
    query = """
    WITH category_yearly AS (
        SELECT
            EXTRACT(YEAR FROM o.purchase_timestamp)::INTEGER AS year,
            COALESCE(p.category_name_english, 'unknown') AS category,

            COUNT(DISTINCT o.order_id) AS orders,
            COUNT(*) AS items,
            SUM(oi.price) AS revenue

        FROM core.fact_order_item oi

        JOIN core.fact_order o
            ON oi.order_key = o.order_key

        JOIN core.dim_product p
            ON oi.product_key = p.product_key

        WHERE EXTRACT(YEAR FROM o.purchase_timestamp)::INTEGER
              IN (%s, %s)

        GROUP BY
            EXTRACT(YEAR FROM o.purchase_timestamp)::INTEGER,
            COALESCE(p.category_name_english, 'unknown')
    ),

    category_comparison AS (
        SELECT
            category,

            MAX(
                CASE
                    WHEN year = %s THEN orders
                    ELSE 0
                END
            ) AS previous_orders,

            MAX(
                CASE
                    WHEN year = %s THEN orders
                    ELSE 0
                END
            ) AS current_orders,

            MAX(
                CASE
                    WHEN year = %s THEN items
                    ELSE 0
                END
            ) AS previous_items,

            MAX(
                CASE
                    WHEN year = %s THEN items
                    ELSE 0
                END
            ) AS current_items,

            MAX(
                CASE
                    WHEN year = %s THEN revenue
                    ELSE 0
                END
            ) AS previous_revenue,

            MAX(
                CASE
                    WHEN year = %s THEN revenue
                    ELSE 0
                END
            ) AS current_revenue

        FROM category_yearly

        GROUP BY category
    )

    SELECT
        category,
        previous_orders,
        current_orders,
        previous_items,
        current_items,
        previous_revenue,
        current_revenue
    FROM category_comparison
    ORDER BY
        (current_revenue - previous_revenue) DESC;
    """

    result = execute_query(
        query,
        (
            previous_year,
            current_year,
            previous_year,
            current_year,
            previous_year,
            current_year,
            previous_year,
            current_year
        )
    )

    return result


def print_category_drivers(current_year, previous_year):
    result = analyze_category_drivers(
        current_year,
        previous_year
    )

    print("CATEGORY REVENUE DRIVER ANALYSIS")
    print("=" * 120)

    for row in result["rows"]:

        (
            category,
            previous_orders,
            current_orders,
            previous_items,
            current_items,
            previous_revenue,
            current_revenue
        ) = row

        previous_orders = int(previous_orders or 0)
        current_orders = int(current_orders or 0)

        previous_items = int(previous_items or 0)
        current_items = int(current_items or 0)

        previous_revenue = float(previous_revenue or 0)
        current_revenue = float(current_revenue or 0)

        previous_items_per_order = (
            previous_items / previous_orders
            if previous_orders
            else 0
        )

        current_items_per_order = (
            current_items / current_orders
            if current_orders
            else 0
        )

        previous_avg_price = (
            previous_revenue / previous_items
            if previous_items
            else 0
        )

        current_avg_price = (
            current_revenue / current_items
            if current_items
            else 0
        )

        revenue_change = current_revenue - previous_revenue

        print(f"\nCategory: {category}")

        print(
            f"  Revenue: "
            f"₹{previous_revenue:,.2f} → "
            f"₹{current_revenue:,.2f} "
            f"(Change: ₹{revenue_change:,.2f})"
        )

        print(
            f"  Orders: "
            f"{previous_orders:,} → "
            f"{current_orders:,}"
        )

        print(
            f"  Items: "
            f"{previous_items:,} → "
            f"{current_items:,}"
        )

        print(
            f"  Items / Order: "
            f"{previous_items_per_order:.2f} → "
            f"{current_items_per_order:.2f}"
        )

        print(
            f"  Average Item Price: "
            f"₹{previous_avg_price:,.2f} → "
            f"₹{current_avg_price:,.2f}"
        )