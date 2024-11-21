# config/config.py

# Database configuration
SQLITE_DB_PATH = "data/database/investor_diary.db"
VECTOR_STORE_PATH = "data/vectorstore/faiss_index"

# Langchain configuration
LANGCHAIN_TRACING_V2 = "true"
LANGCHAIN_ENDPOINT ="https://api.smith.langchain.com"
LANGCHAIN_PROJECT ="investor-diary-project"

# Model configuration 
MODEL_NAME = "gpt-4o-mini"