# src/database/db_utils.py

import sqlite3
from typing import List
from datetime import datetime
from langchain_community.utilities import SQLDatabase
from src.utils.rag_utils import load_vector_store
from config.config import SQLITE_DB_PATH

def get_db_connection():
    return SQLDatabase.from_uri(f"sqlite:///{SQLITE_DB_PATH}")

def check_stock_exists(symbol: str):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT company_name FROM stocks WHERE symbol = ?', (symbol.upper(),))
    result = cursor.fetchone()
    conn.close()
    return result

def add_stock(symbol: str, company_name: str, sector: str) -> str:
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    try:
        result = check_stock_exists(symbol)
        
        if result:
            return f"Stock {symbol} already exists"
        
        cursor.execute('''
            INSERT INTO stocks (symbol, company_name, sector)
            VALUES (?, ?, ?)
        ''', (symbol.upper(), company_name, sector))
        
        conn.commit()
        new_stock_id = cursor.lastrowid
        return f"Successfully added stock {symbol} with ID: {new_stock_id}"
    
    except sqlite3.Error as e:
        conn.rollback()
        return f"Error adding stock: {str(e)}"
    finally:
        conn.close()

def add_record(symbol, transaction_type, quantity, price_per_share, transaction_date, notes):
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    try:
        # Get stock_id
        cursor.execute('SELECT stock_id, company_name FROM stocks WHERE symbol = ?', (symbol.upper(),))
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Stock {symbol} not found in records. Please insert the stock in the records before creating an transactional record.")
        
        stock_id = result[0]
        total_amount = quantity * price_per_share
        
        # Insert transaction
        cursor.execute('''
            INSERT INTO transactions 
            (stock_id, transaction_type, quantity, price_per_share, 
             transaction_date, total_amount, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            stock_id,
            transaction_type.upper(),
            quantity,
            price_per_share,
            transaction_date,
            total_amount,
            notes
        ))
        vectorstore = load_vector_store()
        vectorstore.add_texts([f"The Company: {result[1]} has been {transaction_type}, because of the following reason:\n{notes}"])
        
        conn.commit()
        return f"Successfully added {transaction_type} transaction for {symbol}"
    
    except (sqlite3.Error, ValueError) as e:
        conn.rollback()
        return f"Error adding transaction: {str(e)}"
    finally:
        conn.close()