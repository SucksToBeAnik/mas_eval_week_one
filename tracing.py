"""
Langfuse tracing using @observe decorator.
"""

import os
from dotenv import load_dotenv
from langfuse import Langfuse, observe
from custom_types import Trace

load_dotenv()

def init_langfuse() -> None:
    """Initialize Langfuse with credentials."""
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    base_url = os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com")

    if not secret_key or not public_key:
        raise ValueError("Langfuse credentials must be provided")

    os.environ["LANGFUSE_SECRET_KEY"] = secret_key
    os.environ["LANGFUSE_PUBLIC_KEY"] = public_key
    os.environ["LANGFUSE_HOST"] = base_url

    # Initialize Langfuse client (needed for flushing)
    global _langfuse_client
    _langfuse_client = Langfuse(
        secret_key=secret_key,
        public_key=public_key,
        host=base_url,
    )


_langfuse_client = None


@observe(name="log_trace")
def log_trace_to_langfuse(
    trace: Trace,
    trace_name: str = "llm_trace",
    model: str = "unknown",
    **metadata,
) -> None:
    """
    Log trace to Langfuse using @observe decorator.
    The decorator automatically captures inputs, outputs, and execution time.
    """
    # The @observe decorator automatically captures:
    # - Function inputs (trace, trace_name, model, metadata)
    # - Function output
    # - Execution time
    # All of this is sent to Langfuse automatically

    # Flush to ensure data is sent
    if _langfuse_client:
        _langfuse_client.flush()
