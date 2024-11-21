# src/agents/base_agent.py

from typing_extensions import TypedDict
from typing import Annotated, Dict, List, Literal, Optional
from langgraph.graph.message import AnyMessage, add_messages


def update_dialog_stack(left: list[str], right: str = None) -> list[str]:
    """Push or pop the state."""
    if right is None:
        return left
    if right == "pop":
        return left[:-1]
    return left + [right]


class MainState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    dialog_state: Annotated[
        list[
            Literal[
                "assistant",
                "add_transactions",
                "retrieve_transactions",
                "find_notes",
                "research_stock_news",
            ]
        ],
        update_dialog_stack,
    ]

from langchain_core.runnables import Runnable, RunnableConfig
from pydantic import BaseModel

class CompleteOrEscalate(BaseModel):
    """A tool to mark the current task as completed and/or to escalate control of the dialog to the main assistant"""
    cancel: bool = True
    reason: str

    class Config:
        json_schema_extra = {
            "example": {
                "cancel": True,
                "reason": "User changed their mind about the current task.",
            }
        }

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: MainState, config: RunnableConfig):
        while True:
            result = self.runnable.invoke(state)

            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}