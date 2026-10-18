from src.analytics.sql_generator import (
    generate_seller_revenue_comparison_sql,
    generate_sql
)


TEST_QUESTIONS = [
    "What was our monthly revenue?",
    "Which products generated the highest revenue?",
    "Which sellers generated the highest revenue?",
    "What is the average delivery time?",
    "What is the average review score?",
    "What caused the decline in sales in 2018?",
    "Which products generated the highest revenue in 2017?",
    "Which sellers generated the highest revenue in 2017?",
    "Compare sellers by revenue in 2017",
]


def run_seller_comparison_focused_tests():
    print("=" * 70)
    print("RUNNING FOCUSED SELLER REVENUE COMPARISON TESTS")
    print("=" * 70)

    # 1. Default sorting (sorting omitted or None)
    plan_default_year = {
        "time_period": ["2017"]
    }
    sql_default_year = generate_seller_revenue_comparison_sql(plan_default_year)
    assert "ORDER BY total_revenue DESC" in sql_default_year, "Default sorting must be DESC"
    assert "LIMIT 10;" in sql_default_year, "Default limit must be 10"
    assert "WHERE EXTRACT(YEAR FROM o.purchase_timestamp) = 2017" in sql_default_year, "Year filter must be applied"
    assert "core.fact_order_item oi" in sql_default_year, "Year filter query must use core tables"

    plan_default_lifetime = {
        "source_tables": ["analytics.seller_metrics"]
    }
    sql_default_lifetime = generate_seller_revenue_comparison_sql(plan_default_lifetime)
    assert "ORDER BY total_revenue DESC" in sql_default_lifetime, "Default lifetime sorting must be DESC"
    assert "LIMIT 10;" in sql_default_lifetime, "Default lifetime limit must be 10"
    assert "FROM analytics.seller_metrics" in sql_default_lifetime, "Lifetime comparison must use analytics.seller_metrics"
    assert "WHERE" not in sql_default_lifetime, "Lifetime comparison must not contain WHERE clause"

    # 2. Custom limit
    plan_custom_limit = {
        "time_period": ["2017"],
        "sorting": {"limit": 5}
    }
    sql_custom_limit = generate_seller_revenue_comparison_sql(plan_custom_limit)
    assert "LIMIT 5;" in sql_custom_limit, "Custom limit must be 5"
    assert "ORDER BY total_revenue DESC" in sql_custom_limit, "Direction should default to DESC"

    plan_custom_limit_str = {
        "source_tables": ["analytics.seller_metrics"],
        "sorting": {"limit": "25"}
    }
    sql_custom_limit_str = generate_seller_revenue_comparison_sql(plan_custom_limit_str)
    assert "LIMIT 25;" in sql_custom_limit_str, "String numeric limit must be parsed to 25"

    # 3. Ascending direction
    plan_asc = {
        "time_period": ["2017"],
        "sorting": {"direction": "ASC", "limit": 7}
    }
    sql_asc = generate_seller_revenue_comparison_sql(plan_asc)
    assert "ORDER BY total_revenue ASC" in sql_asc, "Direction must be ASC"
    assert "LIMIT 7;" in sql_asc, "Limit must be 7"

    plan_asc_case = {
        "source_tables": ["analytics.seller_metrics"],
        "sorting": {"direction": "asc"}
    }
    sql_asc_case = generate_seller_revenue_comparison_sql(plan_asc_case)
    assert "ORDER BY total_revenue ASC" in sql_asc_case, "Lowercase 'asc' must be normalized to ASC"
    assert "LIMIT 10;" in sql_asc_case, "Limit must default to 10"

    # 4. Descending direction
    plan_desc = {
        "time_period": ["2017"],
        "sorting": {"direction": "DESC", "limit": 3}
    }
    sql_desc = generate_seller_revenue_comparison_sql(plan_desc)
    assert "ORDER BY total_revenue DESC" in sql_desc, "Direction must be DESC"
    assert "LIMIT 3;" in sql_desc, "Limit must be 3"

    # 5. Invalid / edge case sorting values fallback safely
    plan_invalid_sorting = {
        "time_period": ["2017"],
        "sorting": {"direction": "INVALID_DIR", "limit": -5}
    }
    sql_invalid_sorting = generate_seller_revenue_comparison_sql(plan_invalid_sorting)
    assert "ORDER BY total_revenue DESC" in sql_invalid_sorting, "Invalid direction must fall back to DESC"
    assert "LIMIT 10;" in sql_invalid_sorting, "Negative limit must fall back to 10"

    # 6. Multi-year filter preservation
    plan_multi_year = {
        "time_period": ["2016", "2017"],
        "sorting": {"direction": "DESC", "limit": 15}
    }
    sql_multi_year = generate_seller_revenue_comparison_sql(plan_multi_year)
    assert "WHERE EXTRACT(YEAR FROM o.purchase_timestamp) IN (2016, 2017)" in sql_multi_year, "Multi-year filter must be preserved"
    assert "LIMIT 15;" in sql_multi_year, "Limit must be 15"

    # 7. End-to-end question generation with explicit and default limits
    sql_e2e_default = generate_sql("Compare sellers by revenue in 2017")
    assert "WHERE EXTRACT(YEAR FROM o.purchase_timestamp) = 2017" in sql_e2e_default
    assert "ORDER BY total_revenue DESC" in sql_e2e_default
    assert "LIMIT 10;" in sql_e2e_default

    sql_e2e_top5 = generate_sql("Compare top 5 sellers by revenue")
    assert "analytics.seller_metrics" in sql_e2e_top5
    assert "WHERE" not in sql_e2e_top5
    assert "ORDER BY total_revenue DESC" in sql_e2e_top5
    assert "LIMIT 5;" in sql_e2e_top5

    sql_e2e_top3_2017 = generate_sql("Compare the top 3 sellers by revenue in 2017")
    assert "WHERE EXTRACT(YEAR FROM o.purchase_timestamp) = 2017" in sql_e2e_top3_2017
    assert "ORDER BY total_revenue DESC" in sql_e2e_top3_2017
    assert "LIMIT 3;" in sql_e2e_top3_2017

    print("ALL FOCUSED SELLER REVENUE COMPARISON TESTS PASSED SUCCESSFULLY!\n")


def main():
    run_seller_comparison_focused_tests()

    for question in TEST_QUESTIONS:

        print("=" * 70)
        print("QUESTION:")
        print(question)

        try:
            sql = generate_sql(question)

            print("\nGENERATED SQL:")
            print(sql)

        except Exception as error:

            print("\nERROR:")
            print(error)

        print()


if __name__ == "__main__":
    main()