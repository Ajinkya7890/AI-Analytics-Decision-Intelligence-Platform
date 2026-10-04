from src.analytics.analytical_planner import create_plan
from src.analytics.sql_generator import generate_sql
from src.database.sql_validator import validate_sql
from src.database.query_executor import execute_query
from src.statistics.analyzer import descriptive_statistics


def run_question(question):
    """
    Complete analytical query pipeline.

    Question
        ↓
    Analytical Plan
        ↓
    SQL Generation
        ↓
    SQL Validation
        ↓
    SQL Execution
        ↓
    Statistical Analysis (when required)
        ↓
    Results
    """

    # --------------------------------------------------
    # Step 1 — Create analytical plan
    # --------------------------------------------------

    plan = create_plan(question)

    # --------------------------------------------------
    # Step 2 — Generate SQL
    # --------------------------------------------------

    sql = generate_sql(question)

    # --------------------------------------------------
    # Step 3 — Validate SQL
    # --------------------------------------------------

    is_valid, validation_message = validate_sql(sql)

    if not is_valid:
        raise ValueError(
            f"Generated SQL failed validation: "
            f"{validation_message}"
        )

    # --------------------------------------------------
    # Step 4 — Execute SQL
    # --------------------------------------------------

    result = execute_query(sql)

    columns = result["columns"]
    rows = result["rows"]

    # --------------------------------------------------
    # Step 5 — Statistical analysis
    # --------------------------------------------------

    statistics = None

    if plan["intent"] == "statistical":
        numeric_values = []

        for row in rows:
            for value in row:
                if isinstance(value, (int, float)):
                    numeric_values.append(value)

        if numeric_values:
            statistics = descriptive_statistics(
                numeric_values
            )

    # --------------------------------------------------
    # Step 6 — Return everything needed downstream
    # --------------------------------------------------

    return {
        "question": question,
        "plan": plan,
        "sql": sql,
        "validation": validation_message,
        "columns": columns,
        "rows": rows,
        "statistics": statistics
    }