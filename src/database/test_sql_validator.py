from src.database.sql_validator import validate_sql


test_queries = [
    "SELECT * FROM core.fact_order",

    """
    SELECT
        COUNT(*) AS total_orders
    FROM core.fact_order
    """,

    "WITH orders AS (SELECT * FROM core.fact_order) SELECT COUNT(*) FROM orders",

    "DELETE FROM core.fact_order",

    "DROP TABLE core.fact_order",

    "UPDATE core.fact_order SET order_status = 'x'",

    "SELECT * FROM core.fact_order; DROP TABLE core.fact_order"
]


for query in test_queries:
    valid, message = validate_sql(query)

    print("-" * 60)
    print("Query:")
    print(query)
    print("Valid:", valid)
    print("Message:", message)