from langchain_core.tools import tool
from src.utils.rag_utils import load_vector_store

@tool
def lookup_notes(query: str) -> str:
    """Get the users personal diary notes on his various stock market purchases and sellings over his lifetime."""
    vectorstore = load_vector_store()
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in docs])