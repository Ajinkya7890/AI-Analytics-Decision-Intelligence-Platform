from src.config.database import get_connection


class DimensionRegistry:
    """
    Metadata-driven registry for analytical dimensions.

    Dimensions are defined in:

        metadata.dimensions

    Physical table/column mappings are defined in:

        metadata.dimension_sources
    """

    def __init__(self):
        self._dimensions = self._load_dimensions()

    def _load_dimensions(self):
        """
        Load dimensions and their physical source columns
        from the metadata layer.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    d.dimension_id,
                    d.dataset_id,
                    d.dimension_name,
                    d.dimension_type,
                    d.description,
                    t.table_name,
                    c.column_name,
                    c.data_type,
                    ds.source_role
                FROM metadata.dimensions d
                LEFT JOIN metadata.dimension_sources ds
                    ON d.dimension_id = ds.dimension_id
                LEFT JOIN metadata.tables t
                    ON ds.table_id = t.table_id
                LEFT JOIN metadata.columns c
                    ON ds.column_id = c.column_id
                ORDER BY
                    d.dimension_id,
                    ds.dimension_source_id;
            """)

            rows = cursor.fetchall()

        finally:
            cursor.close()
            connection.close()

        dimensions = {}

        for row in rows:

            (
                dimension_id,
                dataset_id,
                dimension_name,
                dimension_type,
                description,
                table_name,
                column_name,
                data_type,
                source_role
            ) = row

            if dimension_name not in dimensions:

                dimensions[dimension_name] = {
                    "dimension_id": dimension_id,
                    "dataset_id": dataset_id,
                    "name": dimension_name,
                    "type": dimension_type,
                    "description": description,
                    "sources": []
                }

            if table_name and column_name:

                dimensions[dimension_name][
                    "sources"
                ].append({
                    "table_name": table_name,
                    "column_name": column_name,
                    "data_type": data_type,
                    "source_role": source_role
                })

        return dimensions

    def get_dimension(self, dimension_name):
        """
        Return a dimension by canonical name.
        """

        return self._dimensions.get(
            dimension_name
        )

    def has_dimension(self, dimension_name):
        """
        Check whether a dimension exists.
        """

        return dimension_name in self._dimensions

    def get_all_dimensions(self):
        """
        Return all registered dimensions.
        """

        return list(
            self._dimensions.values()
        )

    def get_dimension_names(self):
        """
        Return all canonical dimension names.
        """

        return list(
            self._dimensions.keys()
        )

    def get_sources(self, dimension_name):
        """
        Return all physical sources for a dimension.
        """

        dimension = self.get_dimension(
            dimension_name
        )

        if not dimension:
            return []

        return dimension["sources"]

    def get_source_tables(self, dimension_name):
        """
        Return unique physical tables associated with
        a dimension.
        """

        sources = self.get_sources(
            dimension_name
        )

        return list(
            dict.fromkeys(
                source["table_name"]
                for source in sources
            )
        )

    def get_source_columns(self, dimension_name):
        """
        Return physical source columns associated with
        a dimension.
        """

        return self.get_sources(
            dimension_name
        )


def get_dimension_registry():
    """
    Create and return a metadata-driven dimension registry.
    """

    return DimensionRegistry()