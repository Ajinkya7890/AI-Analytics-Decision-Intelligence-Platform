from src.ai.question_analyzer import analyze_question
from src.metadata.metric_resolver import get_metric_resolver
from src.metadata.dimension_registry import get_dimension_registry


class AnalyticalPlanner:
    """
    Builds an analytical execution plan from a natural-language
    question.

    Metrics and dimensions are resolved through the metadata
    layer instead of being hardcoded inside the planner.
    """

    def __init__(self):
        self.metric_resolver = get_metric_resolver()
        self.dimension_registry = get_dimension_registry()

    def select_source_tables(
        self,
        metrics,
        dimensions
    ):
        """
        Resolve the physical source tables required by the
        requested metrics and dimensions.
        """

        source_tables = []

        # Resolve metric sources.
        for metric in metrics:

            resolved_metric = (
                self.metric_resolver.get_metric(
                    metric
                )
            )

            if not resolved_metric:
                continue

            for table_name in (
                resolved_metric["source_tables"]
            ):

                if table_name not in source_tables:
                    source_tables.append(
                        table_name
                    )

        # Resolve dimension sources.
        for dimension in dimensions:

            dimension_sources = (
                self.dimension_registry.get_source_tables(
                    dimension
                )
            )

            for table_name in dimension_sources:

                if table_name not in source_tables:
                    source_tables.append(
                        table_name
                    )

        return source_tables

    def determine_operations(self, intent):
        """
        Determine analytical operations from the detected
        analytical intent.
        """

        operation_map = {
            "trend_analysis": [
                "time_series_aggregation"
            ],
            "ranking": [
                "aggregation",
                "ranking"
            ],
            "comparison": [
                "group_comparison"
            ],
            "aggregation": [
                "aggregation"
            ],
            "statistical": [
                "statistical_summary"
            ],
            "root_cause": [
                "root_cause_analysis"
            ],
            "unknown": [
                "general_analysis"
            ]
        }

        return operation_map.get(
            intent,
            ["general_analysis"]
        )

    def determine_group_by(self, dimensions):
        """
        Resolve semantic dimensions to their canonical names.

        The physical source columns remain in metadata and are
        resolved later by downstream SQL generation.
        """

        group_by = []

        for dimension in dimensions:

            if not self.dimension_registry.has_dimension(
                dimension
            ):
                continue

            if dimension not in group_by:
                group_by.append(
                    dimension
                )

        return group_by

    def determine_time_granularity(
        self,
        dimensions,
        intent
    ):
        """
        Determine the requested time granularity using the
        registered temporal dimensions.
        """

        if (
            "Month" in dimensions
            and self.dimension_registry.has_dimension(
                "Month"
            )
        ):
            return "month"

        if (
            "Year" in dimensions
            and self.dimension_registry.has_dimension(
                "Year"
            )
        ):
            return "year"

        if intent == "trend_analysis":
            return "time"

        return None

    @staticmethod
    def determine_sorting(intent):
        """
        Determine sorting requirements for the analytical
        operation.
        """

        if intent == "ranking":
            return {
                "direction": "DESC",
                "limit": 10
            }

        if intent == "trend_analysis":
            return {
                "direction": "ASC",
                "limit": None
            }

        return None

    def create_plan(self, question):
        """
        Create an analytical execution plan from a natural-
        language question.
        """

        analysis = analyze_question(
            question
        )

        metrics = analysis["metrics"]
        dimensions = analysis["dimensions"]
        intent = analysis["intent"]
        time_period = analysis["time_period"]
        filters = analysis["filters"]

        source_tables = self.select_source_tables(
            metrics=metrics,
            dimensions=dimensions
        )

        operations = self.determine_operations(
            intent=intent
        )

        group_by = self.determine_group_by(
            dimensions=dimensions
        )

        time_granularity = (
            self.determine_time_granularity(
                dimensions=dimensions,
                intent=intent
            )
        )

        sorting = self.determine_sorting(
            intent=intent
        )

        return {
            "question": question,
            "intent": intent,
            "metrics": metrics,
            "dimensions": dimensions,
            "time_period": time_period,
            "time_granularity": time_granularity,
            "filters": filters,
            "source_tables": source_tables,
            "operations": operations,
            "group_by": group_by,
            "sorting": sorting
        }


def create_plan(question):
    """
    Backward-compatible helper used by existing modules.
    """

    planner = AnalyticalPlanner()

    return planner.create_plan(
        question
    )