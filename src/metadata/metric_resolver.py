import re

from src.metadata.metadata_loader import get_metrics
from src.metadata.analytical_table_registry import (
    get_analytical_table_registry
)


class MetricResolver:
    """
    Resolves business metrics to their physical SQL sources
    using metadata.metrics.

    The resolver extracts schema.table.column references
    from metric SQL expressions and determines the physical
    source tables and available analytical-layer sources.

    This keeps metric-to-source logic outside the analytical
    planner and SQL generator.
    """

    THREE_PART_IDENTIFIER_PATTERN = re.compile(
        r"\b("
        r"[a-zA-Z_][\w]*"
        r"\."
        r"[a-zA-Z_][\w]*"
        r"\."
        r"[a-zA-Z_][\w]*"
        r")\b"
    )

    def __init__(self):
        self.analytical_table_registry = (
            get_analytical_table_registry()
        )

        self._metrics = self._load_metrics()

    def _load_metrics(self):
        """
        Load metric definitions and resolve their physical
        source tables and referenced columns.
        """

        metrics = {}

        for row in get_metrics():

            metric_name = row[0]
            metric_definition = row[1]
            sql_expression = row[2]
            metric_type = row[3]

            source_tables = self._resolve_source_tables(
                sql_expression
            )

            referenced_columns = (
                self._extract_referenced_columns(
                    sql_expression
                )
            )

            analytical_sources = [
                table_name
                for table_name in source_tables
                if self.analytical_table_registry.has_table(
                    table_name
                )
            ]

            metrics[metric_name] = {
                "name": metric_name,
                "definition": metric_definition,
                "sql_expression": sql_expression,
                "metric_type": metric_type,
                "source_tables": source_tables,
                "referenced_columns": referenced_columns,
                "analytical_sources": analytical_sources
            }

        return metrics

    def _resolve_source_tables(self, sql_expression):
        """
        Resolve schema-qualified tables from fully-qualified
        schema.table.column references.

        Example:

            SUM(core.fact_order_item.price)

        resolves to:

            core.fact_order_item
        """

        if not sql_expression:
            return []

        available_analytical_tables = set(
            self.analytical_table_registry.get_table_names()
        )

        referenced_columns = (
            self._extract_referenced_columns(
                sql_expression
            )
        )

        resolved_tables = []

        for reference in referenced_columns:

            parts = reference.split(".")

            if len(parts) != 3:
                continue

            schema_name = parts[0]
            table_name = parts[1]

            qualified_table = (
                f"{schema_name}.{table_name}"
            )

            if qualified_table in resolved_tables:
                continue

            if (
                qualified_table
                in available_analytical_tables
            ):
                resolved_tables.append(
                    qualified_table
                )
                continue

            if schema_name == "core":
                resolved_tables.append(
                    qualified_table
                )

        return resolved_tables

    @classmethod
    def _extract_referenced_columns(cls, sql_expression):
        """
        Extract fully-qualified schema.table.column
        references from a SQL expression.

        Example:

            SUM(core.fact_order_item.price)

        returns:

            [
                "core.fact_order_item.price"
            ]
        """

        if not sql_expression:
            return []

        matches = (
            cls.THREE_PART_IDENTIFIER_PATTERN.findall(
                sql_expression
            )
        )

        return list(
            dict.fromkeys(matches)
        )

    def get_metric(self, metric_name):
        """
        Return resolved metadata for a metric.
        """

        return self._metrics.get(
            metric_name
        )

    def has_metric(self, metric_name):
        """
        Check whether a metric exists.
        """

        return metric_name in self._metrics

    def get_all_metrics(self):
        """
        Return all resolved metrics.
        """

        return list(
            self._metrics.values()
        )

    def get_metric_names(self):
        """
        Return all canonical metric names.
        """

        return list(
            self._metrics.keys()
        )

    def get_source_tables(self, metric_name):
        """
        Return physical source tables referenced by
        the metric.
        """

        metric = self.get_metric(
            metric_name
        )

        if not metric:
            return []

        return metric["source_tables"]

    def get_analytical_sources(self, metric_name):
        """
        Return analytics-layer tables available for
        the metric.
        """

        metric = self.get_metric(
            metric_name
        )

        if not metric:
            return []

        return metric["analytical_sources"]

    def get_referenced_columns(self, metric_name):
        """
        Return fully-qualified columns referenced by
        the metric.
        """

        metric = self.get_metric(
            metric_name
        )

        if not metric:
            return []

        return metric["referenced_columns"]


def get_metric_resolver():
    """
    Create and return a metadata-driven metric resolver.
    """

    return MetricResolver()