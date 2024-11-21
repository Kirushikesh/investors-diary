# src/agents/analysis_agent.py

from langgraph.graph import END
from langgraph.prebuilt import tools_condition

from src.agents.base_agent import Assistant, MainState, CompleteOrEscalate
from src.tools.analysis_tools import retrieve_transactions_tools
from src.prompts.prompt_templates import get_analysis_prompt
from src.utils.common_utils import get_llm
from src.database.db_utils import get_db_connection

def route_analyse_transactions(
    state: MainState,
):
    route = tools_condition(state)
    if route == END:
        return END
    tool_calls = state["messages"][-1].tool_calls
    did_cancel = any(tc["name"] == CompleteOrEscalate.__name__ for tc in tool_calls)
    if did_cancel:
        return "leave_skill"
    return "retrieve_transactions_tools"

llm = get_llm()
db = get_db_connection()
retrieve_transactions_prompt = get_analysis_prompt().partial(table_info = db.table_info)
retrieve_transactions_runnable = retrieve_transactions_prompt | llm.bind_tools(
    retrieve_transactions_tools + [CompleteOrEscalate]
)

AnalysisAgent = Assistant(retrieve_transactions_runnable)