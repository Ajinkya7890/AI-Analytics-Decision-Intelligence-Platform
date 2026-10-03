import re


FORBIDDEN_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE",
    "EXEC",
    "EXECUTE"
}


def validate_sql(query):
    if not query or not query.strip():
        return False, "Query is empty."

    query = query.strip()

    # Remove one trailing semicolon for validation.
    if query.endswith(";"):
        query = query[:-1].rstrip()

    # Only one SQL statement is allowed.
    if ";" in query:
        return False, "Multiple SQL statements are not allowed."

    # Block SQL comments.
    if "--" in query or "/*" in query or "*/" in query:
        return False, "SQL comments are not allowed."

    # Query must start with SELECT or WITH.
    if not re.match(r"^(SELECT|WITH)\b", query, re.IGNORECASE):
        return False, "Only SELECT or WITH queries are allowed."

    # Check forbidden SQL keywords.
    words = re.findall(r"\b[A-Z_]+\b", query.upper())

    for word in words:
        if word in FORBIDDEN_KEYWORDS:
            return False, f"Forbidden SQL operation detected: {word}"

    return True, "SQL query is valid."