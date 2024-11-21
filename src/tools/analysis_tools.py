# src/tools/analysis_tools.py

from langchain_core.tools import tool
from src.database.db_utils import get_db_connection

db = get_db_connection()

@tool
def db_query_tool(query: str) -> str:
    """
    Execute a SQL query against the database and get back the result.
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    """
    result = db.run_no_throw(query)
    if not result:
        return "Error: Query failed. Please rewrite your query and try again."
    return result

retrieve_transactions_tools = [db_query_tool]