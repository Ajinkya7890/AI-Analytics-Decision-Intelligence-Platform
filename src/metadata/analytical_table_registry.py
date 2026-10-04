from src.metadata.metadata_loader import get_columns


class AnalyticalTableRegistry:
    """
    Metadata-driven registry for analytical tables.

    The registry discovers available columns from metadata
    instead of relying on hardcoded table definitions.
    """

    def __init__(self):
        self._tables = self._load_tables()

    def _load_tables(self):
        """
        Load all analytics-layer tables and their columns.
        """

        tables = {}

        for row in get_columns():

            table_name = row[0]

            if not table_name.startswith(
                "analytics."
            ):
                continue

            column = {
                "table_name": row[0],
                "column_name": row[1],
                "data_type": row[2],
                "semantic_type": row[3],
                "column_role": row[4],
                "description": row[5],
                "is_nullable": row[6]
            }

            if table_name not in tables:
                tables[table_name] = {
                    "table_name": table_name,
                    "columns": []
                }

            tables[table_name]["columns"].append(
                column
            )

        return tables

    def get_table(self, table_name):
        """
        Return metadata for a specific analytical table.
        """

        return self._tables.get(
            table_name
        )

    def get_tables(self):
        """
        Return all analytical tables.
        """

        return list(
            self._tables.values()
        )

    def get_table_names(self):
        """
        Return all analytical table names.
        """

        return list(
            self._tables.keys()
        )

    def has_table(self, table_name):
        """
        Check whether an analytical table exists.
        """

        return table_name in self._tables

    def get_columns(self, table_name):
        """
        Return all columns belonging to an analytical table.
        """

        table = self.get_table(
            table_name
        )

        if not table:
            return []

        return table["columns"]

    def has_column(
        self,
        table_name,
        column_name
    ):
        """
        Check whether a table contains a column.
        """

        columns = self.get_columns(
            table_name
        )

        return any(
            column["column_name"] == column_name
            for column in columns
        )

    def get_column_names(self, table_name):
        """
        Return column names available in a table.
        """

        return [
            column["column_name"]
            for column in self.get_columns(
                table_name
            )
        ]

    def find_tables_with_column(
        self,
        column_name
    ):
        """
        Find analytical tables containing a specific column.
        """

        matching_tables = []

        for table_name in self.get_table_names():

            if self.has_column(
                table_name,
                column_name
            ):
                matching_tables.append(
                    table_name
                )

        return matching_tables


def get_analytical_table_registry():
    """
    Create and return the analytical table registry.
    """

    return AnalyticalTableRegistry()