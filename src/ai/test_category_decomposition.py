from src.ai.category_driver_engine import (
    analyze_all_category_drivers
)


results = analyze_all_category_drivers(
    current_year=2018,
    previous_year=2017
)


print("CATEGORY DECOMPOSITION TEST")
print("=" * 100)


for category in results[:10]:

    decomposition = category["decomposition"]
    drivers = category["driver_analysis"]

    print(
        f"\nCategory: {category['category']}"
    )

    print(
        f"Revenue Change: "
        f"₹{category['revenue_change']:,.2f}"
    )

    print(
        f"Order Effect: "
        f"₹{decomposition['order_effect']:,.2f}"
    )

    print(
        f"Items/Order Effect: "
        f"₹{decomposition['items_per_order_effect']:,.2f}"
    )

    print(
        f"Price Effect: "
        f"₹{decomposition['price_effect']:,.2f}"
    )

    print(
        f"Explained Change: "
        f"₹{decomposition['total_explained_change']:,.2f}"
    )

    print(
        f"Primary Negative Driver: "
        f"{drivers['primary_negative_driver']}"
    )

    print(
        f"Primary Positive Driver: "
        f"{drivers['primary_positive_driver']}"
    )