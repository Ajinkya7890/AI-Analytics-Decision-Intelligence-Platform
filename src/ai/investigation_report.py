from src.ai.investigation_result import build_investigation_result


def build_investigation_report(root_cause_result):
    """
    Convert the analytical root-cause result into a
    concise, structured business investigation report.
    """

    investigation = build_investigation_result(root_cause_result)

    overall = investigation["overall"]
    period = investigation["period"]

    report = {
        "period": (
            period["previous_year"],
            period["current_year"]
        ),

        "overall_result": {
            "previous_revenue": overall["previous_revenue"],
            "current_revenue": overall["current_revenue"],
            "revenue_change": overall["revenue_change"],
            "percentage_change": overall["percentage_change"]
        },

        "growth_drivers": [],

        "declining_categories": []
    }

    for contributor in investigation["top_positive_contributors"]:
        report["growth_drivers"].append({
            "category": contributor["category"],
            "revenue_change": contributor["revenue_change"],
            "contribution_pct": contributor["contribution_pct"],
            "primary_driver": contributor["growth_driver"],
            "primary_driver_effect": contributor["growth_driver_effect"],
            "primary_drag": contributor["growth_drag"],
            "primary_drag_effect": contributor["growth_drag_effect"]
        })

    for contributor in investigation["top_negative_contributors"]:
        report["declining_categories"].append({
            "category": contributor["category"],
            "revenue_change": contributor["revenue_change"],
            "contribution_pct": contributor["contribution_pct"],
            "primary_driver": contributor["decline_driver"],
            "primary_driver_effect": contributor["decline_driver_effect"],
            "offset": contributor["decline_offset"],
            "offset_effect": contributor["decline_offset_effect"]
        })

    return report


def print_investigation_report(report):
    """
    Print the structured investigation report
    in a business-readable format.
    """

    previous_year, current_year = report["period"]
    overall = report["overall_result"]

    print("INVESTIGATION REPORT")
    print("=" * 80)

    print(
        f"\nPERIOD: {previous_year} → {current_year}"
    )

    print("\nEXECUTIVE CONCLUSION")
    print("-" * 80)

    print(
        f"Revenue changed from "
        f"₹{overall['previous_revenue']:,.2f} "
        f"to ₹{overall['current_revenue']:,.2f}."
    )

    print(
        f"Revenue change: "
        f"₹{overall['revenue_change']:,.2f} "
        f"({overall['percentage_change']:+.2f}%)"
    )

    print("\nTOP GROWTH DRIVERS")
    print("-" * 80)

    for index, driver in enumerate(
        report["growth_drivers"],
        start=1
    ):
        print(
            f"{index}. {driver['category']}"
        )

        print(
            f"   Revenue contribution: "
            f"₹{driver['revenue_change']:,.2f}"
        )

        print(
            f"   Share of total change: "
            f"{driver['contribution_pct']:.2f}%"
        )

        print(
            f"   Primary driver: "
            f"{driver['primary_driver']} "
            f"(₹{driver['primary_driver_effect']:,.2f})"
        )

        if driver["primary_drag"]:
            print(
                f"   Primary drag: "
                f"{driver['primary_drag']} "
                f"(₹{driver['primary_drag_effect']:,.2f})"
            )

    print("\nTOP DECLINING CATEGORIES")
    print("-" * 80)

    for index, category in enumerate(
        report["declining_categories"],
        start=1
    ):
        print(
            f"{index}. {category['category']}"
        )

        print(
            f"   Revenue change: "
            f"₹{category['revenue_change']:,.2f}"
        )

        print(
            f"   Share of total change: "
            f"{category['contribution_pct']:.2f}%"
        )

        print(
            f"   Decline driver: "
            f"{category['primary_driver']} "
            f"(₹{category['primary_driver_effect']:,.2f})"
        )

        if category["offset"]:
            print(
                f"   Offset: "
                f"{category['offset']} "
                f"(₹{category['offset_effect']:,.2f})"
            )