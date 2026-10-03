def calculate_percentage_change(previous, current):
    if previous == 0:
        if current == 0:
            return 0.0
        return None

    return ((current - previous) / previous) * 100


def classify_driver(
    previous_orders,
    current_orders,
    previous_items_per_order,
    current_items_per_order,
    previous_avg_price,
    current_avg_price
):
    order_change = calculate_percentage_change(
        previous_orders,
        current_orders
    )

    items_per_order_change = calculate_percentage_change(
        previous_items_per_order,
        current_items_per_order
    )

    price_change = calculate_percentage_change(
        previous_avg_price,
        current_avg_price
    )

    changes = {
        "ORDER_VOLUME": order_change,
        "ITEMS_PER_ORDER": items_per_order_change,
        "AVERAGE_PRICE": price_change
    }

    positive_drivers = [
        driver
        for driver, change in changes.items()
        if change is not None and change > 0
    ]

    negative_drivers = [
        driver
        for driver, change in changes.items()
        if change is not None and change < 0
    ]

    ranked_positive_drivers = sorted(
        positive_drivers,
        key=lambda driver: abs(changes[driver]),
        reverse=True
    )

    ranked_negative_drivers = sorted(
        negative_drivers,
        key=lambda driver: abs(changes[driver]),
        reverse=True
    )

    if ranked_positive_drivers:
        primary_driver = ranked_positive_drivers[0]

        if len(ranked_positive_drivers) > 1:
            secondary_driver = ranked_positive_drivers[1]
        else:
            secondary_driver = None

    elif ranked_negative_drivers:
        primary_driver = ranked_negative_drivers[0]
        secondary_driver = (
            ranked_negative_drivers[1]
            if len(ranked_negative_drivers) > 1
            else None
        )

    else:
        primary_driver = "NO_MATERIAL_CHANGE"
        secondary_driver = None

    return {
        "order_change_pct": order_change,
        "items_per_order_change_pct": items_per_order_change,
        "average_price_change_pct": price_change,
        "positive_drivers": positive_drivers,
        "negative_drivers": negative_drivers,
        "ranked_positive_drivers": ranked_positive_drivers,
        "ranked_negative_drivers": ranked_negative_drivers,
        "primary_driver": primary_driver,
        "secondary_driver": secondary_driver
    }