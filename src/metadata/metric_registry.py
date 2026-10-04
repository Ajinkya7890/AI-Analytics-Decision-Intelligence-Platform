from src.metadata.metadata_loader import get_metrics


class MetricRegistry:
    """
    Provides metadata-driven access to the metrics
    available in the current analytical dataset.
    """

    def __init__(self):
        self._metrics = self._load_metrics()

    def _load_metrics(self):
        """
        Load metric definitions from metadata.metrics.
        """

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

    def get_metric(self, metric_name):
        """
        Return metadata for a specific metric.
        """

        return self._metrics.get(metric_name)

    def has_metric(self, metric_name):
        """
        Check whether a metric exists in the current
        analytical metadata.
        """

        return metric_name in self._metrics

    def get_all_metrics(self):
        """
        Return all available metrics.
        """

        return list(self._metrics.values())

    def get_metric_names(self):
        """
        Return the canonical names of all available metrics.
        """

        return list(self._metrics.keys())


def get_metric_registry():
    """
    Create and return a metric registry using the
    currently loaded dataset metadata.
    """

    return MetricRegistry()