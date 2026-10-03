def build_investigation_result(root_cause_result):
    """
    Convert the root-cause engine output into a structured
    investigation result for downstream AI explanation.
    """

    positive_categories = root_cause_result[
        "positive_categories"
    ]

    negative_categories = root_cause_result[
        "negative_categories"
    ]

    top_positive = []

    for category in positive_categories[:5]:

        impact = category["impact_analysis"]
        decomposition = category["decomposition"]

        top_positive.append({
            "category": category["category"],
            "revenue_change": category["revenue_change"],
            "contribution_pct": category["contribution_pct"],

            "growth_driver": (
                impact["growth_driver"][0]
                if impact["growth_driver"]
                else None
            ),

            "growth_driver_effect": (
                impact["growth_driver"][1]
                if impact["growth_driver"]
                else None
            ),

            "growth_drag": (
                impact["growth_drag"][0]
                if impact["growth_drag"]
                else None
            ),

            "growth_drag_effect": (
                impact["growth_drag"][1]
                if impact["growth_drag"]
                else None
            ),

            "order_effect":
                decomposition["order_effect"],

            "items_per_order_effect":
                decomposition["items_per_order_effect"],

            "price_effect":
                decomposition["price_effect"]
        })

    top_negative = []

    for category in negative_categories[:5]:

        impact = category["impact_analysis"]
        decomposition = category["decomposition"]

        top_negative.append({
            "category": category["category"],
            "revenue_change": category["revenue_change"],
            "contribution_pct": category["contribution_pct"],

            "decline_driver": (
                impact["decline_driver"][0]
                if impact["decline_driver"]
                else None
            ),

            "decline_driver_effect": (
                impact["decline_driver"][1]
                if impact["decline_driver"]
                else None
            ),

            "decline_offset": (
                impact["decline_offset"][0]
                if impact["decline_offset"]
                else None
            ),

            "decline_offset_effect": (
                impact["decline_offset"][1]
                if impact["decline_offset"]
                else None
            ),

            "order_effect":
                decomposition["order_effect"],

            "items_per_order_effect":
                decomposition["items_per_order_effect"],

            "price_effect":
                decomposition["price_effect"]
        })

    return {
        "period": {
            "previous_year":
                root_cause_result["previous_year"],

            "current_year":
                root_cause_result["current_year"]
        },

        "overall": {
            "previous_revenue":
                root_cause_result["previous_revenue"],

            "current_revenue":
                root_cause_result["current_revenue"],

            "revenue_change":
                root_cause_result["total_change"],

            "percentage_change":
                root_cause_result["percentage_change"]
        },

        "top_positive_contributors":
            top_positive,

        "top_negative_contributors":
            top_negative
    }


def print_investigation_result(result):

    print("STRUCTURED INVESTIGATION RESULT")
    print("=" * 100)

    period = result["period"]
    overall = result["overall"]

    print(
        f"\nPeriod: "
        f"{period['previous_year']} → "
        f"{period['current_year']}"
    )

    print(
        f"Revenue Change: "
        f"₹{overall['revenue_change']:,.2f}"
    )

    print(
        f"Percentage Change: "
        f"{overall['percentage_change']:.2f}%"
    )

    print("\nTOP POSITIVE CONTRIBUTORS")
    print("-" * 100)

    for item in result["top_positive_contributors"]:

        print(
            f"\n{item['category']}"
        )

        print(
            f"  Revenue Change: "
            f"₹{item['revenue_change']:,.2f}"
        )

        print(
            f"  Contribution: "
            f"{item['contribution_pct']:.2f}%"
        )

        print(
            f"  Growth Driver: "
            f"{item['growth_driver']}"
        )

        print(
            f"  Growth Driver Effect: "
            f"₹{item['growth_driver_effect']:,.2f}"
            if item["growth_driver_effect"] is not None
            else "  Growth Driver Effect: None"
        )

        print(
            f"  Growth Drag: "
            f"{item['growth_drag']}"
        )

        print(
            f"  Growth Drag Effect: "
            f"₹{item['growth_drag_effect']:,.2f}"
            if item["growth_drag_effect"] is not None
            else "  Growth Drag Effect: None"
        )

    print("\nTOP NEGATIVE CONTRIBUTORS")
    print("-" * 100)

    for item in result["top_negative_contributors"]:

        print(
            f"\n{item['category']}"
        )

        print(
            f"  Revenue Change: "
            f"₹{item['revenue_change']:,.2f}"
        )

        print(
            f"  Contribution: "
            f"{item['contribution_pct']:.2f}%"
        )

        print(
            f"  Decline Driver: "
            f"{item['decline_driver']}"
        )

        print(
            f"  Decline Driver Effect: "
            f"₹{item['decline_driver_effect']:,.2f}"
            if item["decline_driver_effect"] is not None
            else "  Decline Driver Effect: None"
        )

        print(
            f"  Decline Offset: "
            f"{item['decline_offset']}"
        )

        print(
            f"  Decline Offset Effect: "
            f"₹{item['decline_offset_effect']:,.2f}"
            if item["decline_offset_effect"] is not None
            else "  Decline Offset Effect: None"
        )