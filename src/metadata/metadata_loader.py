from src.config.database import get_connection


def get_tables():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                table_name,
                table_type,
                description
            FROM metadata.tables
            ORDER BY table_name;
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_columns(table_name=None):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        if table_name:
            cursor.execute("""
                SELECT
                    mt.table_name,
                    mc.column_name,
                    mc.data_type,
                    mc.semantic_type,
                    mc.column_role,
                    mc.description,
                    mc.is_nullable
                FROM metadata.columns mc
                JOIN metadata.tables mt
                    ON mc.table_id = mt.table_id
                WHERE mt.table_name = %s
                ORDER BY mc.column_id;
            """, (table_name,))
        else:
            cursor.execute("""
                SELECT
                    mt.table_name,
                    mc.column_name,
                    mc.data_type,
                    mc.semantic_type,
                    mc.column_role,
                    mc.description,
                    mc.is_nullable
                FROM metadata.columns mc
                JOIN metadata.tables mt
                    ON mc.table_id = mt.table_id
                ORDER BY mt.table_name, mc.column_id;
            """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_relationships():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                source_table,
                source_column,
                target_table,
                target_column,
                relationship_type,
                description
            FROM metadata.relationships
            ORDER BY relationship_id;
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_metrics():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                metric_name,
                metric_definition,
                sql_expression,
                metric_type
            FROM metadata.metrics
            ORDER BY metric_id;
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()