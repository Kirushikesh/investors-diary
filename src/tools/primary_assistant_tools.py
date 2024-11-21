from pydantic import BaseModel, Field
from langchain_community.tools.tavily_search import TavilySearchResults

class AddTransactionAssistant(BaseModel):
    """Transfers work to a specialized assistant to add new stock purchase or selling transactions by the user"""

    request: str = Field(
        description="Any necessary followup questions the transaction assistant should clarify before proceeding."
    )


class RetrieveTransactions(BaseModel):
    """Transfers work to a specialized assistant to retrieve all the investments and exits done by the user."""

    request: str = Field(
        description="Any information or requests from the user analysis on the transactions"
    )


class RetrieveNotes(BaseModel):
    """Transfers work to a specialized assistant to retrieve all the users personal thought process on the stock purchases."""

    request: str = Field(
        description="The user query or request to look on the notes"
    )

class StockResearcher(BaseModel):
    """Transfers work to a specialized assistant to do a detailed research on a particular company based on its recent events."""

    request: str = Field(
        description="The user query to perform research on"
    )

primary_assistant_tools = [
    TavilySearchResults(max_results=1),
    AddTransactionAssistant,
    RetrieveTransactions,
    RetrieveNotes,
    StockResearcher
]