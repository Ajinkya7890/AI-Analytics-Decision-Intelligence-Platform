from abc import ABC, abstractmethod


class InvestigationStrategy(ABC):
    """
    Base interface for analytical investigation strategies.

    Each strategy represents a specific analytical method
    that can investigate a business question.
    """

    name = None
    description = None

    @abstractmethod
    def supports(self, analysis):
        """
        Determine whether this strategy can handle the
        structured question analysis.
        """
        raise NotImplementedError

    @abstractmethod
    def investigate(self, analysis):
        """
        Execute the analytical investigation.
        """
        raise NotImplementedError


class RevenueRootCauseStrategy(InvestigationStrategy):
    """
    Revenue root-cause investigation strategy.

    This strategy currently uses the existing revenue
    root-cause engine developed for the validation dataset.
    """

    name = "revenue_root_cause"

    description = (
        "Analyze revenue change between two periods and "
        "identify the major contributing categories and "
        "underlying revenue drivers."
    )

    def supports(self, analysis):
        """
        Determine whether the question is a metric-level
        revenue root-cause investigation requiring two
        periods.
        """

        if analysis.get("analysis_type") != "metric_root_cause":
            return False

        metrics = analysis.get("metrics", [])

        if "Revenue" not in metrics:
            return False

        time_period = analysis.get("time_period") or []

        if len(time_period) < 2:
            return False

        return True

    def investigate(self, analysis):
        """
        Execute the existing revenue root-cause analysis.
        """

        from src.ai.root_cause_engine import analyze_root_cause
        from src.ai.investigation_result import (
            build_investigation_result
        )

        time_period = analysis["time_period"]

        previous_year = int(time_period[0])
        current_year = int(time_period[1])

        root_cause_result = analyze_root_cause(
            current_year=current_year,
            previous_year=previous_year
        )

        return build_investigation_result(
            root_cause_result
        )


class InvestigationStrategyRegistry:
    """
    Registry containing all available investigation strategies.
    """

    def __init__(self):
        self._strategies = []

    def register(self, strategy):
        """
        Register an investigation strategy.
        """

        if not isinstance(strategy, InvestigationStrategy):
            raise TypeError(
                "strategy must inherit from InvestigationStrategy."
            )

        self._strategies.append(strategy)

    def get_strategy(self, analysis):
        """
        Return the first strategy that supports the analysis.
        """

        for strategy in self._strategies:
            if strategy.supports(analysis):
                return strategy

        return None

    def get_strategies(self):
        """
        Return all registered strategies.
        """

        return list(self._strategies)


def create_default_registry():
    """
    Create the default investigation strategy registry.
    """

    registry = InvestigationStrategyRegistry()

    registry.register(
        RevenueRootCauseStrategy()
    )

    return registry