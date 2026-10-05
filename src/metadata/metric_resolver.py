from src.config.database import get_connection
from src.metadata.metadata_loader import get_metrics


class MetricResolver:
    """
    Metadata-driven registry for analytical metrics.

    Business metric definitions come from:

        metadata.metrics

    Physical analytical metric sources come from:

        metadata.metric_sources
    """

    def __init__(self):
        self._metrics = self._load_metrics()

    def _load_metrics(self):

        metric_definitions = self._load_metric_definitions()
        metric_sources = self._load_metric_sources()

        metrics = {}

        for metric_name, metric in metric_definitions.items():

            sources = metric_sources.get(
                metric_name,
                []
            )

            metrics[metric_name] = {
                "name": metric["name"],
                "definition": metric["definition"],
                "sql_expression": metric["sql_expression"],
                "metric_type": metric["metric_type"],

                "source_tables": list(
                    dict.fromkeys(
                        source["table_name"]
                        for source in sources
                    )
                ),

                "referenced_columns": [
                    (
                        f"{source['table_name']}."
                        f"{source['column_name']}"
                    )
                    for source in sources
                ],

                "analytical_sources": sources
            }

        return metrics

    @staticmethod
    def _load_metric_definitions():

        metrics = {}

        for row in get_metrics():

            metric_name = row[0]
            metric_definition = row[1]
            sql_expression = row[2]
            metric_type = row[3]

            metrics[metric_name] = {
                "name": metric_name,
                "definition": metric_definition,
                "sql_expression": sql_expression,
                "metric_type": metric_type
            }

        return metrics

    @staticmethod
    def _load_metric_sources():

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    m.metric_name,
                    t.table_name,
                    c.column_name,
                    c.data_type,
                    ms.source_role,
                    ms.aggregation_method,
                    ms.source_grain,
                    ms.calculation_expression
                FROM metadata.metric_sources ms
                JOIN metadata.metrics m
                    ON ms.metric_id = m.metric_id
                JOIN metadata.tables t
                    ON ms.table_id = t.table_id
                JOIN metadata.columns c
                    ON ms.column_id = c.column_id
                ORDER BY
                    m.metric_id,
                    ms.metric_source_id;
            """)

            rows = cursor.fetchall()

        finally:

            cursor.close()
            connection.close()

        metric_sources = {}

        for row in rows:

            (
                metric_name,
                table_name,
                column_name,
                data_type,
                source_role,
                aggregation_method,
                source_grain,
                calculation_expression
            ) = row

            if metric_name not in metric_sources:

                metric_sources[metric_name] = []

            metric_sources[metric_name].append({

                "table_name": table_name,

                "column_name": column_name,

                "data_type": data_type,

                "source_role": source_role,

                "aggregation_method": aggregation_method,

                "source_grain": source_grain,

                "calculation_expression":
                    calculation_expression
            })

        return metric_sources

    def get_metric(self, metric_name):
        return self._metrics.get(metric_name)

    def has_metric(self, metric_name):
        return metric_name in self._metrics

    def get_all_metrics(self):
        return list(self._metrics.values())

    def get_metric_names(self):
        return list(self._metrics.keys())

    def get_source_tables(self, metric_name):

        metric = self.get_metric(metric_name)

        if not metric:
            return []

        return metric["source_tables"]

    def get_analytical_sources(self, metric_name):

        metric = self.get_metric(metric_name)

        if not metric:
            return []

        return metric["analytical_sources"]

    def get_referenced_columns(self, metric_name):

        metric = self.get_metric(metric_name)

        if not metric:
            return []

        return metric["referenced_columns"]

    def get_source_metadata(
        self,
        metric_name,
        source_table
    ):
        """
        Return metadata for a specific physical metric source.
        """

        sources = self.get_analytical_sources(
            metric_name
        )

        for source in sources:

            if source["table_name"] == source_table:

                return source

        return None

    def get_aggregation_method(
        self,
        metric_name,
        source_table
    ):
        """
        Return the aggregation method registered for
        a specific metric source.
        """

        source = self.get_source_metadata(
            metric_name,
            source_table
        )

        if not source:
            return None

        return source["aggregation_method"]

    def get_source_grain(
        self,
        metric_name,
        source_table
    ):
        """
        Return the analytical grain registered for
        a metric source.
        """

        source = self.get_source_metadata(
            metric_name,
            source_table
        )

        if not source:
            return None

        return source["source_grain"]

    def get_calculation_expression(
        self,
        metric_name,
        source_table
    ):
        """
        Return the calculation expression registered for
        a specific metric source.
        """

        source = self.get_source_metadata(
            metric_name,
            source_table
        )

        if not source:
            return None

        return source["calculation_expression"]


def get_metric_resolver():
    return MetricResolver()