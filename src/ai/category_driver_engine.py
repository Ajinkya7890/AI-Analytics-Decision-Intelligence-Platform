from src.ai.revenue_drivers import analyze_category_drivers
from src.ai.revenue_decomposition import (
    calculate_decomposition,
    classify_decomposition
)


def analyze_all_category_drivers(current_year, previous_year):
    """
    Analyze revenue drivers for every product category.

    Uses exact values returned from PostgreSQL and applies
    revenue decomposition:

        Revenue = Orders × Items per Order × Average Item Price
    """

    result = analyze_category_drivers(
        current_year=current_year,
        previous_year=previous_year
    )

    categories = []

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

        # Exact Items per Order
        previous_items_per_order = (
            previous_items / previous_orders
            if previous_orders
            else 0.0
        )

        current_items_per_order = (
            current_items / current_orders
            if current_orders
            else 0.0
        )

        # Exact Average Item Price
        previous_avg_price = (
            previous_revenue / previous_items
            if previous_items
            else 0.0
        )

        current_avg_price = (
            current_revenue / current_items
            if current_items
            else 0.0
        )

        # Revenue decomposition
        decomposition = calculate_decomposition(
            previous_orders=previous_orders,
            current_orders=current_orders,
            previous_items_per_order=previous_items_per_order,
            current_items_per_order=current_items_per_order,
            previous_avg_price=previous_avg_price,
            current_avg_price=current_avg_price
        )

        # Driver classification
        driver_analysis = classify_decomposition(
            decomposition
        )

        categories.append({
            "category": category,

            "previous_revenue": previous_revenue,
            "current_revenue": current_revenue,
            "revenue_change": (
                current_revenue - previous_revenue
            ),

            "previous_orders": previous_orders,
            "current_orders": current_orders,

            "previous_items": previous_items,
            "current_items": current_items,

            "previous_items_per_order":
                previous_items_per_order,

            "current_items_per_order":
                current_items_per_order,

            "previous_avg_price":
                previous_avg_price,

            "current_avg_price":
                current_avg_price,

            "decomposition": decomposition,

            "driver_analysis": driver_analysis
        })

    return categories


def print_category_driver_analysis(
    current_year,
    previous_year
):
    results = analyze_all_category_drivers(
        current_year=current_year,
        previous_year=previous_year
    )

    print("CATEGORY REVENUE DECOMPOSITION")
    print("=" * 110)

    for category in results:

        decomposition = category["decomposition"]
        drivers = category["driver_analysis"]

        print(
            f"\n{category['category']}"
        )

        print(
            f"Revenue Change: "
            f"₹{category['revenue_change']:,.2f}"
        )

        print(
            f"Orders: "
            f"{category['previous_orders']:,} → "
            f"{category['current_orders']:,}"
        )

        print(
            f"Items/Order: "
            f"{category['previous_items_per_order']:.4f} → "
            f"{category['current_items_per_order']:.4f}"
        )

        print(
            f"Avg Price: "
            f"₹{category['previous_avg_price']:.2f} → "
            f"₹{category['current_avg_price']:.2f}"
        )

        print("\nDecomposition:")

        print(
            f"  Order Volume Effect: "
            f"₹{decomposition['order_effect']:,.2f}"
        )

        print(
            f"  Items/Order Effect: "
            f"₹{decomposition['items_per_order_effect']:,.2f}"
        )

        print(
            f"  Average Price Effect: "
            f"₹{decomposition['price_effect']:,.2f}"
        )

        print(
            f"  Total Explained Change: "
            f"₹{decomposition['total_explained_change']:,.2f}"
        )

        print(
            f"\nPrimary Negative Driver: "
            f"{drivers['primary_negative_driver']}"
        )

        print(
            f"Primary Positive Driver: "
            f"{drivers['primary_positive_driver']}"
        )