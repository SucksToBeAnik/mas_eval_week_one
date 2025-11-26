from typing import List, TypedDict


class LLMCall(TypedDict):
    prompt: str
    response: str
    start: float
    end: float
    input_tokens: int
    output_tokens: int
    cost: float


class Trace(TypedDict):
    llm_calls: List[LLMCall]
