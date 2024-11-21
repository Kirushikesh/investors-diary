# src/core/app_builder.py

import uuid
import traceback

from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage,  HumanMessage

from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver

from src.utils.common_utils import create_tool_node_with_fallback, _print_event

from src.agents.base_agent import MainState
from src.agents.transaction_agent import TransactionAgent, route_update_transactions
from src.agents.primary_agent import route_primary_assistant, PrimaryAgent
from src.agents.analysis_agent import AnalysisAgent, route_analyse_transactions
from src.agents.dialogue_manager import create_entry_node, pop_dialog_state, route_to_workflow
from src.agents.rag_agent import retrieve_user_stock_notes

from src.tools.primary_assistant_tools import primary_assistant_tools
from src.tools.analysis_tools import retrieve_transactions_tools
from src.tools.transaction_tools import add_transaction_tools

from src.core.research_sub_graph_builder import sub_graph

builder = StateGraph(MainState)

# Add primary assistant nodes
builder.add_node(
    "primary_assistant", PrimaryAgent
)
builder.add_node(
    "primary_assistant_tools", create_tool_node_with_fallback(primary_assistant_tools)
)

# Add transaction nodes
builder.add_node(
    "enter_add_transactions",
    create_entry_node("Stock Entry Assistant", "add_transactions")
)
builder.add_node(
    "add_transactions",
    TransactionAgent
)
builder.add_node(
    "update_transactions_records_tools",
    create_tool_node_with_fallback(add_transaction_tools),
)

# Add analysis nodes
builder.add_node(
    "enter_retrieve_transactions",
    create_entry_node("Transactions Analysis Assistant", "retrieve_transactions")
)
builder.add_node("retrieve_transactions", AnalysisAgent)
builder.add_node(
    "retrieve_transactions_tools",
    create_tool_node_with_fallback(retrieve_transactions_tools),
)

# Add Notes Rag nodes
builder.add_node(
    "enter_find_notes",
    create_entry_node("User Stock Notes Analysis Assistant", "find_notes"),
)
builder.add_node("find_notes", retrieve_user_stock_notes)

# Add research nodes
def research_stock(state: MainState, config: RunnableConfig):
    user_query = state["messages"][-1].content
    response = sub_graph.invoke({"messages": [("user", user_query)]})

    formatted_response = f"""
Answer:
{response["messages"][-1].tool_calls[0]['args']['answer']}
"""
    if('references' in response["messages"][-1].tool_calls[0]['args']):
        formatted_response+=f"""References:
{response["messages"][-1].tool_calls[0]['args']['references']}"""
    return {"messages": [AIMessage(content = formatted_response)]}

builder.add_node(
    "enter_research_stock_news",
    create_entry_node("Stock Researcher Assistant", "research_stock_news"),
)
builder.add_node("research_stock_news", research_stock)

builder.add_conditional_edges(
    "primary_assistant",
    route_primary_assistant,
    [
        "enter_add_transactions",
        "enter_retrieve_transactions",
        "enter_find_notes",
        "enter_research_stock_news",
        "primary_assistant_tools",
        END,
    ],
)
builder.add_edge("primary_assistant_tools", "primary_assistant")
builder.add_conditional_edges(START, route_to_workflow)

builder.add_edge("enter_add_transactions", "add_transactions")
builder.add_edge("update_transactions_records_tools", "add_transactions")
builder.add_conditional_edges(
    "add_transactions",
    route_update_transactions,
    ["update_transactions_records_tools", "leave_skill", END],
)

builder.add_edge("enter_retrieve_transactions", "retrieve_transactions")
builder.add_edge("retrieve_transactions_tools", "retrieve_transactions")
builder.add_conditional_edges(
    "retrieve_transactions",
    route_analyse_transactions,
    [
        "retrieve_transactions_tools",
        "leave_skill",
        END,
    ],
)

builder.add_edge("enter_find_notes","find_notes")
builder.add_edge("find_notes", "leave_skill")

builder.add_edge("enter_research_stock_news","research_stock_news")
builder.add_edge("research_stock_news", "leave_skill")

builder.add_node("leave_skill", pop_dialog_state)
builder.add_edge("leave_skill", "primary_assistant")

memory = MemorySaver()
main_graph = builder.compile(
    checkpointer=memory,
)

if __name__ == "__main__":
    """Start an interactive chat session"""
    thread_id = str(uuid.uuid4())
    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }
    
    _printed = set()
    print("Welcome to Investor's Diary! Type 'exit' to end the conversation.")
    
    while True:
        # question = 'Hi, How are You'
        question = input('\nYou: ')
        if question.lower() == 'exit':
            print("\nThank you for using Investor's Diary!")
            break
            
        try:
            events = main_graph.stream(
                {"messages": ("user", question)}, 
                config, 
                stream_mode="values"
            )
            
            for event in events:
                _print_event(event, _printed)
                
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print(traceback.format_exc())
            print("Please try again with a different question.")