from langfuse import get_client

from custom_types import Trace
from metrics import MetricAggregator, get_registry
from tracing import init_langfuse, log_trace_to_langfuse
from utils import ollama_chat


def main():
    init_langfuse()
    call = ollama_chat("What is 2+2?", model="gemma3:1b")

    trace: Trace = {"llm_calls": [call]}

    registry = get_registry()
    print(f"\nAvailable metrics: {registry.get_all_names()}")


    agg = MetricAggregator(metrics=["latency", "cost", "tokens"])

    result = agg.compute_all(trace)

    log_trace_to_langfuse(trace, trace_name="main_trace", model="gemma3:1b", **result)

    langfuse_client = get_client()
    if langfuse_client:
        langfuse_client.flush()

    print("\n=== METRICS ===")
    for k, v in result.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
