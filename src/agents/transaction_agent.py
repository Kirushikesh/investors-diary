# src/agents/transaction_agent.py

from langgraph.graph import END
from langgraph.prebuilt import tools_condition

from src.utils.common_utils import get_llm
from src.tools.transaction_tools import add_transaction_tools
from src.prompts.prompt_templates import get_transaction_prompt
from src.agents.base_agent import Assistant, MainState, CompleteOrEscalate

def route_update_transactions(
    state: MainState,
):
    route = tools_condition(state)
    if route == END:
        return END
    tool_calls = state["messages"][-1].tool_calls
    did_cancel = any(tc["name"] == CompleteOrEscalate.__name__ for tc in tool_calls)
    if did_cancel:
        return "leave_skill"
    return "update_transactions_records_tools"

llm = get_llm()
add_transaction_prompt = get_transaction_prompt()
add_transaction_runnable = add_transaction_prompt | llm.bind_tools(
    add_transaction_tools + [CompleteOrEscalate]
)

TransactionAgent = Assistant(add_transaction_tools)