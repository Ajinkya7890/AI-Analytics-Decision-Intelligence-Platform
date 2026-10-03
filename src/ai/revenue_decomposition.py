def calculate_decomposition(
    previous_orders,
    current_orders,
    previous_items_per_order,
    current_items_per_order,
    previous_avg_price,
    current_avg_price
):
    """
    Decompose revenue change into the effects of:

    1. Order volume
    2. Items per order
    3. Average item price

    Revenue model:

        Revenue = Orders × Items/Order × Average Price

    The decomposition uses a sequential approach:
        Step 1: Change orders
        Step 2: Change items/order
        Step 3: Change average price
    """

    previous_revenue = (
        previous_orders
        * previous_items_per_order
        * previous_avg_price
    )

    current_revenue = (
        current_orders
        * current_items_per_order
        * current_avg_price
    )

    # Effect of order volume
    order_effect = (
        (current_orders - previous_orders)
        * previous_items_per_order
        * previous_avg_price
    )

    # Effect of items per order
    items_per_order_effect = (
        current_orders
        * (current_items_per_order - previous_items_per_order)
        * previous_avg_price
    )

    # Effect of average price
    price_effect = (
        current_orders
        * current_items_per_order
        * (current_avg_price - previous_avg_price)
    )

    total_explained_change = (
        order_effect
        + items_per_order_effect
        + price_effect
    )

    return {
        "previous_revenue": previous_revenue,
        "current_revenue": current_revenue,
        "revenue_change": current_revenue - previous_revenue,
        "order_effect": order_effect,
        "items_per_order_effect": items_per_order_effect,
        "price_effect": price_effect,
        "total_explained_change": total_explained_change
    }


def classify_decomposition(decomposition):
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

    primary_negative_driver = (
        ranked_negative[0][0]
        if ranked_negative
        else None
    )

    secondary_negative_driver = (
        ranked_negative[1][0]
        if len(ranked_negative) > 1
        else None
    )

    primary_positive_driver = (
        ranked_positive[0][0]
        if ranked_positive
        else None
    )

    return {
        "effects": effects,
        "positive_effects": ranked_positive,
        "negative_effects": ranked_negative,
        "primary_negative_driver": primary_negative_driver,
        "secondary_negative_driver": secondary_negative_driver,
        "primary_positive_driver": primary_positive_driver
    }