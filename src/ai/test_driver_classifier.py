from src.ai.driver_classifier import classify_driver


result = classify_driver(
    previous_orders=3389,
    current_orders=5402,
    previous_items_per_order=1.08,
    current_items_per_order=1.10,
    previous_avg_price=131.34,
    current_avg_price=129.77
)

print("DRIVER CLASSIFICATION")
print("=" * 60)

for key, value in result.items():
    print(f"{key}: {value}")