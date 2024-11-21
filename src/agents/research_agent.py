# src/agents/research_agent.py
from langgraph.graph import END
from langchain_core.tools import StructuredTool

from src.prompts.prompt_templates import get_research_prompt, revise_research_instructions
from src.utils.common_utils import get_llm
from src.tools.research_tools import AnswerQuestion, ReviseAnswer, tavily_tool
from src.agents.base_agent import Assistant

MAX_ITERATIONS = 2

llm = get_llm()
actor_prompt_template = get_research_prompt()

first_responder = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer.",
    function_name=AnswerQuestion.__name__,
) | llm.bind_tools(tools=[AnswerQuestion])

revisor = actor_prompt_template.partial(
    first_instruction=revise_research_instructions,
    function_name=ReviseAnswer.__name__,
) | llm.bind_tools(tools=[ReviseAnswer])

def run_queries(search_queries: list[str], **kwargs):
    """Run the generated queries."""
    return tavily_tool.batch([{"query": query} for query in search_queries])

research_agents_tools = [
    StructuredTool.from_function(run_queries, name=AnswerQuestion.__name__),
    StructuredTool.from_function(run_queries, name=ReviseAnswer.__name__),
]

def _get_num_iterations(state: list):
    i = 0
    for m in state[::-1]:
        if m.type not in {"tool", "ai"}:
            break
        i += 1
    return i

def event_loop(state: list):
    # in our case, we'll just stop after N plans
    num_iterations = _get_num_iterations(state["messages"])
    if num_iterations > MAX_ITERATIONS:
        return END
    return "execute_tools"

ResearchAgent = Assistant(first_responder)
RevisorAgent = Assistant(revisor)