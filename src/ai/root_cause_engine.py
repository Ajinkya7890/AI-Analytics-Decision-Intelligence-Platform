from src.ai.root_cause import compare_years
from src.ai.category_driver_engine import analyze_all_category_drivers


def calculate_contribution(revenue_change, total_change):
    if total_change == 0:
        return 0.0

    return (revenue_change / total_change) * 100


def classify_category_impact(category):
    """
    Classify category impact based on actual revenue decomposition.

    For revenue growth:
        - Growth driver = largest positive effect
        - Growth drag   = largest negative effect

    For revenue decline:
        - Decline driver = largest negative effect
        - Decline offset = largest positive effect
    """

    decomposition = category["decomposition"]

    effects = {
        "ORDER_VOLUME": decomposition["order_effect"],
        "ITEMS_PER_ORDER": decomposition["items_per_order_effect"],
        "AVERAGE_PRICE": decomposition["price_effect"]
    }

    positive_effects = {
        key: value
        for key, value in effects.items()
        if value > 0
    }

    negative_effects = {
        key: value
        for key, value in effects.items()
        if value < 0
    }

    ranked_positive = sorted(
        positive_effects.items(),
        key=lambda x: x[1],
        reverse=True
    )

    ranked_negative = sorted(
        negative_effects.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )

    revenue_change = category["revenue_change"]

    if revenue_change > 0:

        impact_type = "GROWTH"

        growth_driver = (
            ranked_positive[0]
            if ranked_positive
            else None
        )

        growth_drag = (
            ranked_negative[0]
            if ranked_negative
            else None
        )

        return {
            "impact_type": impact_type,
            "growth_driver": growth_driver,
            "growth_drag": growth_drag
        }

    elif revenue_change < 0:

        impact_type = "DECLINE"

        decline_driver = (
            ranked_negative[0]
            if ranked_negative
            else None
        )

        decline_offset = (
            ranked_positive[0]
            if ranked_positive
            else None
        )

        return {
            "impact_type": impact_type,
            "decline_driver": decline_driver,
            "decline_offset": decline_offset
        }

    return {
        "impact_type": "NO_CHANGE",
        "growth_driver": None,
        "growth_drag": None,
        "decline_driver": None,
        "decline_offset": None
    }


def analyze_root_cause(current_year, previous_year):

    baseline = compare_years(
        current_year=current_year,
        previous_year=previous_year
    )

    total_change = (
        baseline["current_revenue"]
        - baseline["previous_revenue"]
    )

    categories = analyze_all_category_drivers(
        current_year=current_year,
        previous_year=previous_year
    )

    for category in categories:

        category["contribution_pct"] = calculate_contribution(
            category["revenue_change"],
            total_change
        )

        category["impact_analysis"] = (
            classify_category_impact(category)
        )

    positive_categories = [
        category
        for category in categories
        if category["revenue_change"] > 0
    ]

    negative_categories = [
        category
        for category in categories
        if category["revenue_change"] < 0
    ]

    positive_categories.sort(
        key=lambda x: x["revenue_change"],
        reverse=True
    )

    negative_categories.sort(
        key=lambda x: x["revenue_change"]
    )

    return {
        "previous_year": previous_year,
        "current_year": current_year,

        "previous_revenue":
            baseline["previous_revenue"],

        "current_revenue":
            baseline["current_revenue"],

        "total_change":
            total_change,

        "percentage_change":
            baseline["percentage_change"],

        "positive_categories":
            positive_categories,

        "negative_categories":
            negative_categories
    }


def print_root_cause_analysis(current_year, previous_year):

    result = analyze_root_cause(
        current_year=current_year,
        previous_year=previous_year
    )

    print("ROOT-CAUSE ANALYSIS")
    print("=" * 110)

    print(
        f"\nPeriod: "
        f"{result['previous_year']} → "
        f"{result['current_year']}"
    )

    print(
        f"Previous Revenue: "
        f"₹{result['previous_revenue']:,.2f}"
    )

    print(
        f"Current Revenue: "
        f"₹{result['current_revenue']:,.2f}"
    )

    print(
        f"Revenue Change: "
        f"₹{result['total_change']:,.2f}"
    )

    print(
        f"Percentage Change: "
        f"{result['percentage_change']:.2f}%"
    )

    print("\nTOP POSITIVE CONTRIBUTORS")
    print("-" * 110)

    for category in result["positive_categories"][:10]:

        impact = category["impact_analysis"]

        print(
            f"\n{category['category']}"
        )

        print(
            f"  Revenue Change: "
            f"₹{category['revenue_change']:,.2f}"
        )

        print(
            f"  Contribution: "
            f"{category['contribution_pct']:.2f}%"
        )

        if impact["growth_driver"]:

            driver, effect = impact["growth_driver"]

            print(
                f"  Growth Driver: "
                f"{driver} "
                f"(+₹{effect:,.2f})"
            )

        if impact["growth_drag"]:

            drag, effect = impact["growth_drag"]

            print(
                f"  Growth Drag: "
                f"{drag} "
                f"(₹{effect:,.2f})"
            )

    print("\nTOP NEGATIVE CONTRIBUTORS")
    print("-" * 110)

    for category in result["negative_categories"][:10]:

        impact = category["impact_analysis"]

        print(
            f"\n{category['category']}"
        )

        print(
            f"  Revenue Change: "
            f"₹{category['revenue_change']:,.2f}"
        )

        print(
            f"  Contribution: "
            f"{category['contribution_pct']:.2f}%"
        )

        if impact["decline_driver"]:

            driver, effect = impact["decline_driver"]

            print(
                f"  Decline Driver: "
                f"{driver} "
                f"(₹{effect:,.2f})"
            )

        if impact["decline_offset"]:

            offset, effect = impact["decline_offset"]

            print(
                f"  Decline Offset: "
                f"{offset} "
                f"(+₹{effect:,.2f})"
            )