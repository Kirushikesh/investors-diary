# src/utils/rag_utils.py

import sqlite3
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from config.config import VECTOR_STORE_PATH, SQLITE_DB_PATH

def get_notes(top_k=None):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    query = '''
        SELECT s.company_name, t.transaction_type, t.notes
        FROM transactions t
        JOIN stocks s ON t.stock_id = s.stock_id
    '''
    
    if top_k:
        query += f' LIMIT {top_k}'
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return [f"The Company: {transaction[0]} has been {'bought' if transaction[1]=='BUY' else 'sold'}, because of the following reason:\n{transaction[2]}" for transaction in results]

def create_vector_store():
    """Create a vector store from existing records"""
    splits = get_notes()
    vectorstore = FAISS.from_texts(texts=splits, embedding=OpenAIEmbeddings())
    vectorstore.save_local(VECTOR_STORE_PATH)
    return vectorstore

def load_vector_store():
    """Load the existing vector store"""
    return FAISS.load_local(
        VECTOR_STORE_PATH, OpenAIEmbeddings(), allow_dangerous_deserialization=True
    )