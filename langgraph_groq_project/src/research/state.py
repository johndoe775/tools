from typing import List, Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    """Represents the state of our graph."""
    messages: Annotated[List, add_messages]
    inputs: str
    choice: str
    answer: str
    tool_choice: str
