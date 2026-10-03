def format_currency(value):
    """
    Format a numeric value as Indian Rupee currency.
    """
    if value is None:
        return "N/A"

    sign = "-" if value < 0 else ""

    return f"{sign}₹{abs(value):,.2f}"


def format_percentage(value):
    """
    Format a percentage with two decimal places.
    """
    if value is None:
        return "N/A"

    sign = "+" if value > 0 else ""

    return f"{sign}{value:.2f}%"


def format_effect(value):
    """
    Format an analytical effect with an explicit sign.
    """
    if value is None:
        return "N/A"

    if value > 0:
        return f"+₹{value:,.2f}"

    if value < 0:
        return f"-₹{abs(value):,.2f}"

    return "₹0.00"


def format_investigation_evidence(investigation_result):
    """
    Convert structured investigation results into
    controlled evidence for downstream AI explanation.
    """

    overall = investigation_result["overall"]
    period = investigation_result["period"]

    lines = []

    lines.append(
        f"Analysis period: "
        f"{period['previous_year']} to "
        f"{period['current_year']}"
    )

    lines.append(
        f"Previous revenue: "
        f"{format_currency(overall['previous_revenue'])}"
    )

    lines.append(
        f"Current revenue: "
        f"{format_currency(overall['current_revenue'])}"
    )

    lines.append(
        f"Revenue change: "
        f"{format_effect(overall['revenue_change'])}"
    )

    lines.append(
        f"Revenue growth: "
        f"{format_percentage(overall['percentage_change'])}"
    )

    lines.append("")
    lines.append("TOP GROWTH CONTRIBUTORS")

    for index, item in enumerate(
        investigation_result["top_positive_contributors"],
        start=1
    ):

        lines.append(
            f"{index}. {item['category']}"
        )

        lines.append(
            f"   Revenue contribution: "
            f"{format_effect(item['revenue_change'])}"
        )

        lines.append(
            f"   Share of total revenue change: "
            f"{item['contribution_pct']:.2f}%"
        )

        if item["growth_driver"]:
            lines.append(
                f"   Growth driver: "
                f"{item['growth_driver']} "
                f"({format_effect(item['growth_driver_effect'])})"
            )

        if item["growth_drag"]:
            lines.append(
                f"   Growth drag: "
                f"{item['growth_drag']} "
                f"({format_effect(item['growth_drag_effect'])})"
            )

    lines.append("")
    lines.append("TOP DECLINING CONTRIBUTORS")

    for index, item in enumerate(
        investigation_result["top_negative_contributors"],
        start=1
    ):

        lines.append(
            f"{index}. {item['category']}"
        )

        lines.append(
            f"   Revenue contribution: "
            f"{format_effect(item['revenue_change'])}"
        )

        lines.append(
            f"   Share of total revenue change: "
            f"{item['contribution_pct']:.2f}%"
        )

        if item["decline_driver"]:
            lines.append(
                f"   Decline driver: "
                f"{item['decline_driver']} "
                f"({format_effect(item['decline_driver_effect'])})"
            )

        if item["decline_offset"]:
            lines.append(
                f"   Decline offset: "
                f"{item['decline_offset']} "
                f"({format_effect(item['decline_offset_effect'])})"
            )

    return "\n".join(lines)