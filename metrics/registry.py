"""
Global metric registry for automatic metric discovery.
"""

from typing import Dict, List, Type
from metrics.base import MetricPlugin


class MetricRegistry:
    """Global registry for metric plugins."""

    def __init__(self):
        self._metrics: Dict[str, Type[MetricPlugin]] = {}

    def register(self, metric_class: Type[MetricPlugin]) -> Type[MetricPlugin]:
        """
        Register a metric class.

        Args:
            metric_class: The metric class to register

        Returns:
            The metric class (for use as decorator)
        """
        # Create an instance to get the name
        instance = metric_class()
        metric_name = instance.name()

        if metric_name in self._metrics:
            raise ValueError(
                f"Metric '{metric_name}' is already registered. "
                f"Use a different name or unregister the existing one."
            )

        self._metrics[metric_name] = metric_class
        return metric_class

    def get(self, name: str) -> Type[MetricPlugin]:
        """
        Get a metric class by name.

        Args:
            name: The name of the metric

        Returns:
            The metric class

        Raises:
            KeyError: If the metric is not found
        """
        if name not in self._metrics:
            raise KeyError(
                f"Metric '{name}' not found in registry. "
                f"Available metrics: {list(self._metrics.keys())}"
            )
        return self._metrics[name]

    def get_all(self) -> List[Type[MetricPlugin]]:
        """
        Get all registered metric classes.

        Returns:
            List of all registered metric classes
        """
        return list(self._metrics.values())

    def get_all_names(self) -> List[str]:
        """
        Get names of all registered metrics.

        Returns:
            List of metric names
        """
        return list(self._metrics.keys())

    def create_instance(self, name: str) -> MetricPlugin:
        """
        Create an instance of a metric by name.

        Args:
            name: The name of the metric

        Returns:
            An instance of the metric
        """
        metric_class = self.get(name)
        return metric_class()

    def create_instances(self, names: List[str] | None = None) -> List[MetricPlugin]:
        """
        Create instances of metrics.

        Args:
            names: Optional list of metric names. If None, creates all registered metrics.

        Returns:
            List of metric instances
        """
        if names is None:
            names = self.get_all_names()

        return [self.create_instance(name) for name in names]

    def unregister(self, name: str) -> None:
        """
        Unregister a metric.

        Args:
            name: The name of the metric to unregister
        """
        if name in self._metrics:
            del self._metrics[name]

    def clear(self) -> None:
        """Clear all registered metrics."""
        self._metrics.clear()

    def is_registered(self, name: str) -> bool:
        """
        Check if a metric is registered.

        Args:
            name: The name of the metric

        Returns:
            True if registered, False otherwise
        """
        return name in self._metrics


# Global registry instance
_registry = MetricRegistry()


def register_metric(metric_class: Type[MetricPlugin] | None = None):
    """
    Decorator to register a metric class.

    Usage:
        @register_metric
        class MyMetric(MetricPlugin):
            def name(self) -> str:
                return "my_metric"

            def compute(self, trace: Trace) -> float:
                return 42.0

    Or with explicit name:
        @register_metric()
        class MyMetric(MetricPlugin):
            ...
    """

    def decorator(cls: Type[MetricPlugin]) -> Type[MetricPlugin]:
        return _registry.register(cls)

    if metric_class is None:
        # Called as @register_metric
        return decorator
    else:
        # Called as @register_metric()
        return decorator(metric_class)


def get_registry() -> MetricRegistry:
    """
    Get the global metric registry.

    Returns:
        The global MetricRegistry instance
    """
    return _registry


def get_metric(name: str) -> Type[MetricPlugin]:
    """Get a metric class by name from the registry."""
    return _registry.get(name)


def get_all_metrics() -> List[Type[MetricPlugin]]:
    """Get all registered metric classes."""
    return _registry.get_all()


def create_metric(name: str) -> MetricPlugin:
    """Create an instance of a metric by name."""
    return _registry.create_instance(name)


def create_metrics(names: List[str] | None = None) -> List[MetricPlugin]:
    """Create instances of metrics."""
    return _registry.create_instances(names)
