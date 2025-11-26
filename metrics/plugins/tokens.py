from custom_types import Trace
from metrics.base import MetricPlugin
from metrics.registry import register_metric


@register_metric
class TokenMetric(MetricPlugin):
    def name(self) -> str:
        return "tokens"

    def compute(self, trace: Trace) -> float:
        total_input = sum(c["input_tokens"] for c in trace["llm_calls"])
        total_output = sum(c["output_tokens"] for c in trace["llm_calls"])
        return total_input + total_output
