from src.metadata.metadata_loader import (
    get_tables,
    get_columns,
    get_relationships,
    get_metrics
)


print("\n=== TABLES ===")

for table in get_tables():
    print(table)


print("\n=== COLUMNS ===")

columns = get_columns()

for column in columns[:20]:
    print(column)


print("\n=== RELATIONSHIPS ===")

for relationship in get_relationships():
    print(relationship)


print("\n=== METRICS ===")

for metric in get_metrics():
    print(metric)