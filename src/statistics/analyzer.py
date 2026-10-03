from statistics import mean, median, stdev


def clean_numeric_values(values):
    """
    Remove None values and convert numeric values to float.
    """

    cleaned = []

    for value in values:
        if value is not None:
            cleaned.append(float(value))

    return cleaned


def descriptive_statistics(values):
    """
    Calculate descriptive statistics for a numeric series.
    """

    values = clean_numeric_values(values)

    if not values:
        return {
            "count": 0,
            "mean": None,
            "median": None,
            "standard_deviation": None,
            "minimum": None,
            "maximum": None
        }

    result = {
        "count": len(values),
        "mean": mean(values),
        "median": median(values),
        "standard_deviation": (
            stdev(values) if len(values) > 1 else 0.0
        ),
        "minimum": min(values),
        "maximum": max(values)
    }

    return result


def percentage_change(old_value, new_value):
    """
    Calculate percentage change from old_value to new_value.
    """

    if old_value == 0:
        return None

    return ((new_value - old_value) / old_value) * 100