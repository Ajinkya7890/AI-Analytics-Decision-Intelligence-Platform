from src.ai.revenue_decomposition import (
    calculate_decomposition,
    classify_decomposition
)


result = calculate_decomposition(
    previous_orders=3389,
    current_orders=5402,
    previous_items_per_order=1.08,
    current_items_per_order=1.10,
    previous_avg_price=131.34,
    current_avg_price=129.77
)

classification = classify_decomposition(result)


print("REVENUE DECOMPOSITION")
print("=" * 80)

print(f"Previous Revenue: ₹{result['previous_revenue']:,.2f}")
print(f"Current Revenue: ₹{result['current_revenue']:,.2f}")
print(f"Revenue Change: ₹{result['revenue_change']:,.2f}")

print("\nEFFECTS")
print("-" * 80)

for driver, effect in classification["effects"].items():
    print(f"{driver}: ₹{effect:,.2f}")

print("\nPRIMARY NEGATIVE DRIVER:")
print(classification["primary_negative_driver"])

print("\nPRIMARY POSITIVE DRIVER:")
print(classification["primary_positive_driver"])

print("\nTOTAL EXPLAINED CHANGE:")
print(f"₹{result['total_explained_change']:,.2f}")