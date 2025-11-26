from custom_types import Trace
from metrics.base import MetricPlugin
from metrics.registry import register_metric


@register_metric
class CostMetric(MetricPlugin):
    def name(self) -> str:
        return "cost"

    def compute(self, trace: Trace) -> float:
        """Sum all API call costs."""
        return sum(call["cost"] for call in trace["llm_calls"])
