# src/agents/analysis_agent.py

from langgraph.graph import END
from langgraph.prebuilt import tools_condition

from src.agents.base_agent import Assistant, MainState, CompleteOrEscalate
from src.tools.primary_assistant_tools import AddTransactionAssistant, RetrieveTransactions, RetrieveNotes, StockResearcher, primary_assistant_tools
from src.prompts.prompt_templates import get_primary_assistant_prompt
from src.utils.common_utils import get_llm
from src.database.db_utils import get_db_connection

def route_primary_assistant(
    state: MainState,
):
    route = tools_condition(state)
    if route == END:
        return END
    tool_calls = state["messages"][-1].tool_calls
    if tool_calls:
        if tool_calls[0]["name"] == AddTransactionAssistant.__name__:
            return "enter_add_transactions"
        elif tool_calls[0]["name"] == RetrieveTransactions.__name__:
            return "enter_retrieve_transactions"
        elif tool_calls[0]["name"] == RetrieveNotes.__name__:
            return "enter_find_notes"
        elif tool_calls[0]["name"] == StockResearcher.__name__:
            return "enter_research_stock_news"
        return "primary_assistant_tools"
    raise ValueError("Invalid route")

llm = get_llm()
primary_assistant_prompt = get_primary_assistant_prompt()
assistant_runnable = primary_assistant_prompt | llm.bind_tools(
    primary_assistant_tools
)

PrimaryAgent = Assistant(assistant_runnable)