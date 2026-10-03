from src.analytics.sql_generator import generate_sql
from src.database.sql_validator import validate_sql
from src.database.query_executor import execute_query


def run_question(question):
    """
    Complete analytical query pipeline.

    Question
        ↓
    SQL Generation
        ↓
    SQL Validation
        ↓
    SQL Execution
        ↓
    Results
    """

    # --------------------------------------------------
    # Step 1 — Generate SQL
    # --------------------------------------------------

    sql = generate_sql(question)

    # --------------------------------------------------
    # Step 2 — Validate SQL
    # --------------------------------------------------

    is_valid, validation_message = validate_sql(sql)

    if not is_valid:
        raise ValueError(
            f"Generated SQL failed validation: "
            f"{validation_message}"
        )

    # --------------------------------------------------
    # Step 3 — Execute SQL
    # --------------------------------------------------

    result = execute_query(sql)

    # --------------------------------------------------
    # Step 4 — Return everything needed downstream
    # --------------------------------------------------

    return {
        "question": question,
        "sql": sql,
        "validation": validation_message,
        "columns": result["columns"],
        "rows": result["rows"]
    }