from statistics import mean, median, stdev, variance


def clean_numeric_values(*values):
    """
    Remove None values and convert numeric values to float.
    """

    cleaned = []

    for value in values:
        if value is not None:
            cleaned.append(float(value))

    return cleaned


def descriptive_statistics(*values):
    """
    Calculate descriptive statistics for a numeric series.
    """

    values = clean_numeric_values(*values)

    if not values:
        return {
            "count": 0,
            "mean": None,
            "median": None,
            "standard_deviation": None,
            "variance": None,
            "minimum": None,
            "maximum": None,
            "percentile_25": None,
            "percentile_75": None
        }

    result = {
        "count": len(values),
        "mean": mean(values),
        "median": median(values),
        "standard_deviation": (
            stdev(values) if len(values) > 1 else 0.0
        ),
        "variance": (
            variance(values) if len(values) > 1 else 0.0
        ),
        "minimum": min(values),
        "maximum": max(values),
        "percentile_25": calculate_percentile(values, 25),
        "percentile_75": calculate_percentile(values, 75)
    }

    return result


def calculate_percentile(values, percentile):
    """
    Calculate a percentile using linear interpolation.
    """

    values = sorted(clean_numeric_values(*values))

    if not values:
        return None

    if percentile <= 0:
        return values[0]

    if percentile >= 100:
        return values[-1]

    position = (len(values) - 1) * (percentile / 100)

    lower_index = int(position)
    upper_index = lower_index + 1

    if upper_index >= len(values):
        return values[lower_index]

    lower_value = values[lower_index]
    upper_value = values[upper_index]

    fraction = position - lower_index

    return lower_value + (
        (upper_value - lower_value) * fraction
    )


def percentage_change(old_value, new_value):
    """
    Calculate percentage change from old_value to new_value.
    """

    if old_value == 0:
        return None

    return ((new_value - old_value) / old_value) * 100