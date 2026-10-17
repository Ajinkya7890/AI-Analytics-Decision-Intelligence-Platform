from src.ai.query_pipeline import (
    extract_metric_values,
    run_question
)


questions = [
    "What was our monthly revenue?",
    "Which products generated the highest revenue?",
    "What is the average delivery time?",
    "What is the on-time delivery rate?",
    "What is the repeat customer rate?",
    "What is the monthly on-time delivery rate?",
    "What is the average order value?",
    "What was our revenue in 2017?",
    "How many orders were placed in 2017?",
    "What was our monthly revenue in 2017?"
]


def run_tests():
    for question in questions:

        print("\n" + "=" * 80)
        print("QUESTION:")
        print(question)

        try:
            result = run_question(question)

            print("\nSQL:")
            print(result["sql"])

            print("\nVALIDATION:")
            print(result["validation"])

            print("\nCOLUMNS:")
            print(result["columns"])

            print("\nRESULTS (first 5):")
            for row in result["rows"][:5]:
                print(row)

            if result["statistics"]:
                print("\nSTATISTICS:")
                for stat_name, stat_val in result["statistics"].items():
                    print(f"  {stat_name}: {stat_val}")

        except Exception as error:
            print("\nERROR:")
            print(error)
            raise error

    # -------------------------------------------------------------
    # Focused assertion tests for metric result column mappings
    # -------------------------------------------------------------

    # On-Time Delivery Rate extraction tests
    values_ontime_alias = extract_metric_values(
        "On-Time Delivery Rate",
        ["month", "on_time_delivery_rate"],
        [("2017-01-01", 93.5), ("2017-02-01", 94.2)]
    )
    assert values_ontime_alias == [93.5, 94.2], "Should extract on_time_delivery_rate alias"

    values_ontime_col = extract_metric_values(
        "On-Time Delivery Rate",
        ["is_on_time"],
        [(True,), (False,), (True,)]
    )
    assert values_ontime_col == [True, False, True], "Should extract is_on_time column"

    # Repeat Customer Rate extraction tests
    values_repeat_alias = extract_metric_values(
        "Repeat Customer Rate",
        ["month", "repeat_customer_rate"],
        [("2017-01-01", 3.1), ("2017-02-01", 3.4)]
    )
    assert values_repeat_alias == [3.1, 3.4], "Should extract repeat_customer_rate alias"

    values_repeat_col = extract_metric_values(
        "Repeat Customer Rate",
        ["repeat_customer"],
        [(True,), (False,)]
    )
    assert values_repeat_col == [True, False], "Should extract repeat_customer column"

    # -------------------------------------------------------------
    # Focused assertion tests for derived ratio query semantics
    # -------------------------------------------------------------

    # 1. Overall On-Time Delivery Rate (scalar aggregate)
    res_ontime = run_question("What is the on-time delivery rate?")
    assert len(res_ontime["rows"]) == 1, "Overall rate must be a single scalar result"
    assert res_ontime["columns"] == ["on_time_delivery_rate"]
    assert 93.0 <= float(res_ontime["rows"][0][0]) <= 94.0

    # 2. Overall Repeat Customer Rate (scalar aggregate)
    res_repeat = run_question("What is the repeat customer rate?")
    assert len(res_repeat["rows"]) == 1, "Overall rate must be a single scalar result"
    assert res_repeat["columns"] == ["repeat_customer_rate"]
    assert 3.0 <= float(res_repeat["rows"][0][0]) <= 3.3

    # 3. Monthly On-Time Delivery Rate (grouped monthly rates)
    res_monthly_ontime = run_question("What is the monthly on-time delivery rate?")
    assert len(res_monthly_ontime["rows"]) > 1, "Monthly rates must contain multiple group rows"
    assert res_monthly_ontime["columns"] == ["month", "on_time_delivery_rate"]

    # 4. Monthly Repeat Customer Rate (documented architectural limitation)
    try:
        run_question("What is the monthly repeat customer rate?")
        raise AssertionError("Should have raised ValueError for customer_metrics without Month dimension")
    except ValueError as e:
        assert "No compatible analytical source table was found" in str(e)

    # 5. Distribution of On-Time Delivery Rate without grouping (requires grouping dimension)
    try:
        run_question("What is the distribution of on-time delivery rate?")
        raise AssertionError("Should have raised ValueError for ungrouped derived-ratio distribution")
    except ValueError as e:
        assert "requires a grouping dimension" in str(e)

    # 6. Distribution of Repeat Customer Rate without grouping (requires grouping dimension)
    try:
        run_question("What is the distribution of repeat customer rate?")
        raise AssertionError("Should have raised ValueError for ungrouped derived-ratio distribution")
    except ValueError as e:
        assert "requires a grouping dimension" in str(e)

    # 7. Distribution of Average Order Value without grouping (requires grouping dimension)
    try:
        run_question("What is the distribution of average order value?")
        raise AssertionError("Should have raised ValueError for ungrouped derived-ratio distribution")
    except ValueError as e:
        assert "requires a grouping dimension" in str(e)

    # 8. Existing Average Order Value query returns scalar aggregate value intact
    res_aov = run_question("What is the average order value?")
    assert len(res_aov["rows"]) == 1
    assert res_aov["columns"] == ["average_order_value"]
    assert 155.0 <= float(res_aov["rows"][0][0]) <= 165.0

    # -------------------------------------------------------------
    # Focused assertion tests for time-period filtering (Chunk 4)
    # -------------------------------------------------------------

    # 1. "What was our revenue in 2017?"
    res_rev_2017 = run_question("What was our revenue in 2017?")
    assert "WHERE EXTRACT(YEAR FROM full_date) = 2017" in res_rev_2017["sql"], "SQL must filter by 2017"
    assert len(res_rev_2017["rows"]) == 1, "Must return single scalar aggregate"
    assert res_rev_2017["columns"] == ["total_revenue"]
    assert float(res_rev_2017["rows"][0][0]) == 6155806.98, f"Expected 6155806.98, got {res_rev_2017['rows'][0][0]}"

    # 2. "How many orders were placed in 2017?"
    res_orders_2017 = run_question("How many orders were placed in 2017?")
    assert "WHERE EXTRACT(YEAR FROM full_date) = 2017" in res_orders_2017["sql"], "SQL must filter by 2017"
    assert len(res_orders_2017["rows"]) == 1, "Must return single scalar aggregate"
    assert res_orders_2017["columns"] == ["total_orders"]
    assert res_orders_2017["rows"][0][0] == 44579, f"Expected 44579, got {res_orders_2017['rows'][0][0]}"

    # 3. "What was our monthly revenue in 2017?"
    res_monthly_rev_2017 = run_question("What was our monthly revenue in 2017?")
    assert "WHERE EXTRACT(YEAR FROM full_date) = 2017" in res_monthly_rev_2017["sql"], "SQL must filter by 2017"
    assert len(res_monthly_rev_2017["rows"]) == 12, "2017 must have exactly 12 monthly rows"
    assert res_monthly_rev_2017["columns"] == ["month", "revenue"]
    assert all(row[0].year == 2017 for row in res_monthly_rev_2017["rows"]), "All rows must be in year 2017"
    total_monthly_2017 = sum(float(row[1]) for row in res_monthly_rev_2017["rows"])
    assert round(total_monthly_2017, 2) == 6155806.98, f"Monthly sum must match annual revenue 6155806.98, got {total_monthly_2017}"

    # 4. Unconstrained queries preserve existing behavior (e.g. all-time monthly revenue spans all years)
    res_monthly_unconstrained = run_question("What was our monthly revenue?")
    assert "WHERE" not in res_monthly_unconstrained["sql"], "Unconstrained monthly revenue must not have WHERE filter"
    assert len(res_monthly_unconstrained["rows"]) > 12, "Unconstrained monthly revenue spans multiple years (2016-2018)"

    # 5. Unsupported time filter raises actionable error
    try:
        run_question("What is the repeat customer rate in 2017?")
        raise AssertionError("Should have raised ValueError when table has no date column for time filtering")
    except ValueError as e:
        assert "supporting time-period filter" in str(e)

    # 6. Non-empty time-period constraint with no valid years raises actionable error
    from src.analytics.sql_generator import build_time_period_filter, generate_generic_aggregation_sql
    try:
        build_time_period_filter("analytics.daily_sales", ["invalid_year", "not_a_year"])
        raise AssertionError("Should have raised ValueError when time_period contains no valid year values")
    except ValueError as e:
        assert "does not contain any valid year values" in str(e)

    try:
        generate_generic_aggregation_sql({
            "metrics": ["Revenue"],
            "dimensions": [],
            "source_tables": ["analytics.daily_sales"],
            "time_period": ["invalid_year"]
        })
        raise AssertionError("Should have raised ValueError for plan with invalid year values")
    except ValueError as e:
        assert "does not contain any valid year values" in str(e)

    # 7. Year-constrained product rankings, seller rankings, and seller comparisons using core tables
    res_prod_rank_2017 = run_question("Which products generated the highest revenue in 2017?")
    assert "core.fact_order_item oi" in res_prod_rank_2017["sql"], "Product ranking must use core.fact_order_item"
    assert "core.dim_product p" in res_prod_rank_2017["sql"], "Product ranking must join core.dim_product"
    assert "WHERE EXTRACT(YEAR FROM o.purchase_timestamp) = 2017" in res_prod_rank_2017["sql"], "Product ranking must filter by purchase_timestamp year"
    assert len(res_prod_rank_2017["rows"]) == 10, "Product ranking must return 10 rows"
    assert res_prod_rank_2017["columns"] == ["product_id", "category_name_english", "total_revenue"]
    # Verify true 2017 top product is d6160fb7873f184099d9bc95e30376af (48,899.34), not lifetime top bb50f2e236e5eea0100680137654686c
    top_product_id = res_prod_rank_2017["rows"][0][0]
    top_product_rev = float(res_prod_rank_2017["rows"][0][2])
    assert top_product_id == "d6160fb7873f184099d9bc95e30376af", f"Expected top product d6160fb7873f184099d9bc95e30376af, got {top_product_id}"
    assert top_product_rev == 48899.34, f"Expected 48899.34, got {top_product_rev}"

    # Seller ranking for 2017
    res_seller_rank_2017 = run_question("Which sellers generated the highest revenue in 2017?")
    assert "core.fact_order_item oi" in res_seller_rank_2017["sql"], "Seller ranking must use core.fact_order_item"
    assert "core.dim_seller s" in res_seller_rank_2017["sql"], "Seller ranking must join core.dim_seller"
    assert "WHERE EXTRACT(YEAR FROM o.purchase_timestamp) = 2017" in res_seller_rank_2017["sql"], "Seller ranking must filter by purchase_timestamp year"
    assert len(res_seller_rank_2017["rows"]) == 10, "Seller ranking must return 10 rows"
    assert res_seller_rank_2017["columns"] == ["seller_id", "city", "state", "total_revenue"]
    # Verification that the query sums revenue from the requested year (181,113.92) rather than lifetime revenue (222,776.05)
    top_seller_id = res_seller_rank_2017["rows"][0][0]
    top_seller_rev = float(res_seller_rank_2017["rows"][0][3])
    assert top_seller_id == "53243585a1d6dc2643021fd1853d8905", f"Expected top seller 53243585a1d6dc2643021fd1853d8905, got {top_seller_id}"
    assert top_seller_rev == 181113.92, f"Expected 2017 revenue 181113.92, got {top_seller_rev}"

    # Regression case proving that an entity first sold in 2016 can still appear in the 2017 ranking:
    # Seller 7e93a43ef30c4f03f38b393420bc753a had first sale in 2016 (2016-10-08) and earned 159,389.13 in 2017 (rank #2).
    seller_ids_2017 = [row[0] for row in res_seller_rank_2017["rows"]]
    assert "7e93a43ef30c4f03f38b393420bc753a" in seller_ids_2017, "Seller first sold in 2016 must appear in 2017 ranking"
    seller_2016_cohort_row = [r for r in res_seller_rank_2017["rows"] if r[0] == "7e93a43ef30c4f03f38b393420bc753a"][0]
    assert float(seller_2016_cohort_row[3]) == 159389.13, f"Expected 2017 revenue 159389.13, got {seller_2016_cohort_row[3]}"

    # Seller comparison for 2017
    res_seller_comp_2017 = run_question("Compare sellers by revenue in 2017")
    assert "WHERE EXTRACT(YEAR FROM o.purchase_timestamp) = 2017" in res_seller_comp_2017["sql"], "Seller comparison must filter by year"
    assert len(res_seller_comp_2017["rows"]) == 10, "Seller comparison must return rows"
    assert res_seller_comp_2017["columns"] == ["seller_id", "city", "state", "total_revenue"]
    assert float(res_seller_comp_2017["rows"][0][3]) == 181113.92

    # 8. Unconstrained rankings preserve behavior using existing analytical tables without WHERE filter
    res_prod_rank_unconstrained = run_question("Which products generated the highest revenue?")
    assert "analytics.product_metrics" in res_prod_rank_unconstrained["sql"], "Unconstrained product ranking must use analytics.product_metrics"
    assert "WHERE" not in res_prod_rank_unconstrained["sql"], "Unconstrained product ranking must not contain WHERE"
    assert res_prod_rank_unconstrained["rows"][0][0] == "bb50f2e236e5eea0100680137654686c", "Unconstrained returns lifetime top product"

    res_seller_rank_unconstrained = run_question("Which sellers generated the highest revenue?")
    assert "analytics.seller_metrics" in res_seller_rank_unconstrained["sql"], "Unconstrained seller ranking must use analytics.seller_metrics"
    assert "WHERE" not in res_seller_rank_unconstrained["sql"], "Unconstrained seller ranking must not contain WHERE"
    assert res_seller_rank_unconstrained["rows"][0][0] == "4869f7a5dfa277a7dca6462dcf3b52b2", "Unconstrained returns lifetime top seller"

    print("\nALL QUERY PIPELINE TESTS AND ASSERTIONS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_tests()