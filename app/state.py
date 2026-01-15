from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

def merge_dict(a: dict, b: dict) -> dict:
    if a is None: a = {}
    if b is None: b = {}
    # Gộp dict b vào dict a, các key mới sẽ được thêm vào
    res = a.copy()
    res.update(b)
    return res

class TravelState(TypedDict):
    messages: Annotated[list, add_messages]
    user_input: str
    next_step: str
    plan_data: Annotated[dict, merge_dict]