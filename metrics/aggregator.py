from typing import Dict, List, Union

from custom_types import Trace
from metrics.base import MetricPlugin
from metrics.registry import create_metrics


class MetricAggregator:
    """
    Aggregates metrics from a trace.

    Initialize with:
    - List of metric instances: metrics=[CostMetric(), LatencyMetric()]
    - List of metric names (strings): metrics=["cost", "latency"] - pulls from registry
    """

    def __init__(
        self,
        metrics: List[Union[MetricPlugin, str]],
    ):
        """
        Initialize the aggregator.

        Args:
            metrics: List of metric instances or metric names (strings).
        """
        # Check if we have strings (names) or instances
        metric_instances = []
        for item in metrics:
            if isinstance(item, str):
                # It's a metric name - pull from registry
                metric_instances.append(create_metrics([item])[0])
            elif isinstance(item, MetricPlugin):
                # It's already an instance
                metric_instances.append(item)
            else:
                raise TypeError(
                    f"Metric must be a MetricPlugin instance or string name, got {type(item)}"
                )
        self.metrics = metric_instances

    def compute_all(self, trace: Trace) -> Dict[str, float]:
        """
        Compute all metrics for a trace.

        Args:
            trace: The trace to compute metrics for

        Returns:
            Dictionary mapping metric names to their computed values
        """
        results = {}
        for metric in self.metrics:
            results[metric.name()] = metric.compute(trace)
        return results
