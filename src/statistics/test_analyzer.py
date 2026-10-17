from src.statistics.analyzer import (
    clean_numeric_values,
    descriptive_statistics,
    percentage_change
)


def run_tests():
    values = [
        100,
        120,
        150,
        130,
        200
    ]

    print("VALUES:")
    print(values)

    print("\nDESCRIPTIVE STATISTICS (List input):")
    statistics = descriptive_statistics(values)

    for key, value in statistics.items():
        print(f"{key}: {value}")

    print("\nPERCENTAGE CHANGE:")
    change = percentage_change(100, 150)
    print(f"100 -> 150: {change:.2f}%")

    # -------------------------------------------------------------
    # Focused test suite for input contracts
    # -------------------------------------------------------------

    # 1. List input vs unpacked individual arguments produce identical results
    stats_list = descriptive_statistics([100, 120, 150, 130, 200])
    stats_args = descriptive_statistics(100, 120, 150, 130, 200)
    assert stats_list == stats_args, "List input and individual arguments must produce identical statistics"
    assert stats_list["count"] == 5
    assert stats_list["mean"] == 140.0
    assert stats_list["median"] == 130.0
    assert stats_list["minimum"] == 100.0
    assert stats_list["maximum"] == 200.0

    # 2. Missing values (None) in list and individual arguments are filtered
    stats_none_list = descriptive_statistics([100, None, 120, None, 150, 130, 200])
    stats_none_args = descriptive_statistics(100, None, 120, None, 150, 130, 200)
    assert stats_none_list == stats_list, "None values in list must be cleaned"
    assert stats_none_args == stats_list, "None values in arguments must be cleaned"

    # 3. Single value inputs
    stats_single_val = descriptive_statistics(100)
    stats_single_list = descriptive_statistics([100])
    assert stats_single_val == stats_single_list
    assert stats_single_val["count"] == 1
    assert stats_single_val["mean"] == 100.0
    assert stats_single_val["standard_deviation"] == 0.0

    # 4. Empty inputs return 0 count and None metrics
    stats_empty_list = descriptive_statistics([])
    stats_empty_args = descriptive_statistics()
    assert stats_empty_list == stats_empty_args
    assert stats_empty_list["count"] == 0
    assert stats_empty_list["mean"] is None
    assert stats_empty_list["median"] is None

    # 5. Invalid values raise ValueError
    try:
        clean_numeric_values("invalid_non_numeric")
        raise AssertionError("Should have raised ValueError for non-numeric string")
    except ValueError:
        pass

    try:
        clean_numeric_values(["100", "invalid_non_numeric"])
        raise AssertionError("Should have raised ValueError for non-numeric element in list")
    except ValueError:
        pass

    # 6. Percentage change edge cases
    assert percentage_change(0, 100) is None, "Zero old_value must return None"
    assert percentage_change(200, 100) == -50.0

    print("\nALL FOCUSED TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_tests()