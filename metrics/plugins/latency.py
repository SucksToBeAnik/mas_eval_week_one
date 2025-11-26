from custom_types import Trace
from metrics.base import MetricPlugin
from metrics.registry import register_metric


@register_metric
class LatencyMetric(MetricPlugin):
    def name(self) -> str:
        return "latency"

    def compute(self, trace: Trace) -> float:
        """Total latency across all LLM calls."""
        total = 0.0
        for call in trace["llm_calls"]:
            total += call["end"] - call["start"]
        return total
