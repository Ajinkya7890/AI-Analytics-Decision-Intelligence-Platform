from src.config.database import get_connection


def execute_query(query, params=None):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(query, params)

        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()

        return {
            "columns": columns,
            "rows": rows
        }

    finally:
        cursor.close()
        connection.close()