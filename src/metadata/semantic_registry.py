from src.metadata.metric_registry import get_metric_registry
from src.metadata.dimension_registry import get_dimension_registry


class SemanticRegistry:
    """
    Unified semantic registry for the active analytical dataset.

    This layer sits between natural-language understanding and
    physical database metadata.

    It provides:

        Natural-language concept
                ↓
        Canonical business concept
                ↓
        Dataset metadata
    """

    def __init__(self):
        self.metric_registry = get_metric_registry()
        self.dimension_registry = get_dimension_registry()

    def get_metrics(self):
        """
        Return all available canonical metrics.
        """

        return self.metric_registry.get_metric_names()

    def get_dimensions(self):
        """
        Return all available canonical dimensions.
        """

        return self.dimension_registry.get_dimension_names()

    def has_metric(self, metric_name):
        """
        Check whether a metric exists in the active dataset.
        """

        return self.metric_registry.has_metric(
            metric_name
        )

    def has_dimension(self, dimension_name):
        """
        Check whether a dimension exists in the active dataset.
        """

        return self.dimension_registry.has_dimension(
            dimension_name
        )

    def get_metric(self, metric_name):
        """
        Return metadata for a canonical metric.
        """

        return self.metric_registry.get_metric(
            metric_name
        )

    def get_dimension(self, dimension_name):
        """
        Return metadata for a canonical dimension.
        """

        return self.dimension_registry.get_dimension(
            dimension_name
        )

    def resolve_metric(self, candidate, aliases=None):
        """
        Resolve a candidate metric to a canonical metric
        available in the active dataset.

        Example:

            candidate = "sales"

            aliases =
                {
                    "sales": "Revenue"
                }

            result:
                "Revenue"
        """

        if self.has_metric(candidate):
            return candidate

        if not aliases:
            return None

        canonical_metric = aliases.get(
            candidate.lower()
        )

        if canonical_metric and self.has_metric(
            canonical_metric
        ):
            return canonical_metric

        return None

    def resolve_dimension(self, candidate, aliases=None):
        """
        Resolve a candidate dimension to a canonical dimension
        available in the active dataset.
        """

        if self.has_dimension(candidate):
            return candidate

        if not aliases:
            return None

        canonical_dimension = aliases.get(
            candidate.lower()
        )

        if canonical_dimension and self.has_dimension(
            canonical_dimension
        ):
            return canonical_dimension

        return None


def get_semantic_registry():
    """
    Create and return the semantic registry for the
    currently active analytical dataset.
    """

    return SemanticRegistry()