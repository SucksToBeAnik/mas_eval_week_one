import time
from functools import wraps
from typing import Callable

import tiktoken
from langfuse import observe
from langfuse.openai import OpenAI

from custom_types import LLMCall

# Try to get encoding for the model, fallback to cl100k_base (GPT-4) if model not found
try:
    encoding = tiktoken.get_encoding("cl100k_base")
except Exception:
    encoding = tiktoken.encoding_for_model("gpt-4")


def count_tokens(text: str) -> int:
    """Count tokens using tiktoken."""
    return len(encoding.encode(text))


def latency_decorator(func: Callable) -> Callable:
    """
    Decorator to measure latency of a function call.
    Adds start and end time tracking to the function result.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        # If result is a dict (like LLMCall), update timing
        if isinstance(result, dict):
            result["start"] = start
            result["end"] = end

        return result

    return wrapper


@observe(name="ollama_chat", as_type="generation")
@latency_decorator
def ollama_chat(
    prompt: str,
    model: str = "llama3.1",
) -> LLMCall:
    """
    Makes real LLM call to Ollama using the Python API and returns LLMCall dict.
    Uses tiktoken for accurate token counting.
    Latency is automatically tracked by the latency_decorator.

    Args:
        prompt: The prompt to send to the LLM
        model: The model name to use

    Returns:
        LLMCall dict with prompt, response, timing, tokens, and cost
    """
    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    )

    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )

    response_text = response.choices[0].message.content

    input_tokens = count_tokens(prompt)
    output_tokens = count_tokens(response_text)

    cost = (input_tokens + output_tokens) * 0.000001

    llm_call = {
        "prompt": prompt,
        "response": response_text,
        "start": 0.0,  # Will be overwritten by decorator
        "end": 0.0,  # Will be overwritten by decorator
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost": cost,
    }

    return llm_call
