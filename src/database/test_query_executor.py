from src.database.query_executor import execute_query


query = """
SELECT
    COUNT(*) AS total_orders,
    MIN(purchase_timestamp) AS first_order,
    MAX(purchase_timestamp) AS last_order
FROM core.fact_order;
"""


result = execute_query(query)

print("Columns:")
print(result["columns"])

print("\nResult:")
for row in result["rows"]:
    print(row)