from src.ai.query_evidence_formatter import format_query_results


columns = [
    "product_id",
    "category_name_english",
    "total_revenue"
]

rows = [
    (
        "bb50f2e236e5eea0100680137654686c",
        "health_beauty",
        63885.00
    ),
    (
        "6cdd53843498f92890544667809f1595",
        "health_beauty",
        54730.20
    )
]


formatted = format_query_results(
    columns=columns,
    rows=rows
)

print("QUERY EVIDENCE FORMATTER TEST")
print("=" * 80)
print(formatted)