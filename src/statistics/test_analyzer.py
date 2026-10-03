from src.statistics.analyzer import (
    descriptive_statistics,
    percentage_change
)


values = [
    100,
    120,
    150,
    130,
    200
]


print("VALUES:")
print(values)


print("\nDESCRIPTIVE STATISTICS:")

statistics = descriptive_statistics(values)

for key, value in statistics.items():
    print(f"{key}: {value}")


print("\nPERCENTAGE CHANGE:")

change = percentage_change(100, 150)

print(f"100 → 150: {change:.2f}%")