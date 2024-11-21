from src.agents.base_agent import MainState
from langchain_core.messages import AIMessage
from src.tools.rag_tools import lookup_notes
from langchain_core.runnables import RunnableConfig

def retrieve_user_stock_notes(state: MainState, config: RunnableConfig):
    user_query = state["messages"][-1].content
    relevant_chunks = lookup_notes.invoke(user_query)

    return {"messages": [AIMessage(content = relevant_chunks)]}