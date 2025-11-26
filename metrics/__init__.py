"""
Metrics package - provides metric plugins and registry.
"""

from metrics.aggregator import MetricAggregator
from metrics.base import MetricPlugin

# Import plugins to register them
from metrics.plugins import cost, latency, tokens  # noqa: F401
from metrics.registry import (
    create_metric,
    create_metrics,
    get_all_metrics,
    get_metric,
    get_registry,
    register_metric,
)

__all__ = [
    "MetricPlugin",
    "MetricAggregator",
    "register_metric",
    "get_registry",
    "get_metric",
    "get_all_metrics",
    "create_metric",
    "create_metrics",
]
