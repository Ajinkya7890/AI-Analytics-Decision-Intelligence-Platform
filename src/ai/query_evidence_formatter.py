from decimal import Decimal
from datetime import date, datetime


def format_value(value):
    """
    Convert database values into clean business-readable text.
    """

    if value is None:
        return "N/A"

    if isinstance(value, Decimal):
        return f"{value:,.2f}"

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    if isinstance(value, float):
        return f"{value:,.4f}"

    return str(value)


def format_query_results(columns, rows):
    """
    Convert generic SQL query results into structured,
    business-readable evidence.
    """

    lines = []

    for index, row in enumerate(rows, start=1):

        lines.append(f"{index}.")

        for column, value in zip(columns, row):

            lines.append(
                f"   {column}: {format_value(value)}"
            )

    if not lines:
        return "No rows returned."

    return "\n".join(lines)


def format_statistics(statistics):
    """
    Convert verified statistical results into
    business-readable evidence.
    """

    if not statistics:
        return "No statistical analysis available."

    lines = []

    for metric, value in statistics.items():

        formatted_metric = metric.replace("_", " ").title()

        lines.append(
            f"{formatted_metric}: {format_value(value)}"
        )

    return "\n".join(lines)


def format_evidence(columns, rows, statistics=None):
    """
    Build a complete evidence package containing
    SQL query results and optional statistical analysis.
    """

    sections = []

    sections.append(
        "QUERY RESULTS\n"
        "==============\n"
        f"{format_query_results(columns, rows)}"
    )

    if statistics:
        sections.append(
            "STATISTICAL ANALYSIS\n"
            "====================\n"
            f"{format_statistics(statistics)}"
        )

    return "\n\n".join(sections)