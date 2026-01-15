from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

def merge_dict(a: dict, b: dict) -> dict:
    if a is None:
        return b
    if b is None:
        return a
    return {**a, **b}

class TravelState(TypedDict):
    # Dùng cho streaming / debug / demo
    messages: Annotated[list, add_messages]

    # Input gốc từ user
    user_input: str

    # Điều hướng agent
    next_step: str

    # Data tích lũy từ các agent
    plan_data: Annotated[dict, merge_dict]
