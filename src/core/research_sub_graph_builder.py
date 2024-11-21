from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages
from langgraph.graph import END, StateGraph, START

from src.agents.research_agent import research_agents_tools, ResearchAgent, RevisorAgent, event_loop
from src.utils.common_utils import create_tool_node_with_fallback, _print_event

from IPython.display import Image, display

class SUBState(TypedDict):
    messages: Annotated[list, add_messages]

sub_builder = StateGraph(SUBState)
sub_builder.add_node("draft", ResearchAgent)


sub_builder.add_node("execute_tools", create_tool_node_with_fallback(research_agents_tools))
sub_builder.add_node("revise", RevisorAgent)

sub_builder.add_edge("draft", "execute_tools")
sub_builder.add_edge("execute_tools", "revise")

sub_builder.add_conditional_edges("revise", event_loop, ["execute_tools", END])
sub_builder.add_edge(START, "draft")

sub_graph = sub_builder.compile()

if __name__ == "__main__":
    try:
        display(Image(sub_graph.get_graph().draw_mermaid_png()))
    except Exception:
        # This requires some extra dependencies and is optional
        pass
    
    _printed = set()
    print("Welcome to Stock Research Assistant!")
    
    question  = "Who is the current chairman of TATA groups? What happened to the old one?"
        
    try:
        events = sub_graph.stream(
            {"messages": ("user", question)}, 
            stream_mode="values"
        )
        
        for event in events:
            _print_event(event, _printed)
            
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("Please try again with a different question.")

    print("\nThank you for using your research assistant!")
