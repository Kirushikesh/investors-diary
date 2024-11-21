# src/tools/transaction_tools.py

from typing import Annotated
from langchain_core.tools import tool
from datetime import datetime
from src.database.db_utils import check_stock_exists, add_stock, add_record

@tool
def check_stock_present(
    symbol: Annotated[str, "the stock symbol"]
) -> str:
    """Check if the stock has been present in the records based on the stock symbol"""
    result = check_stock_exists(symbol)
    if result:
        return f"Stock {symbol} found"
    return f"Stock {symbol} not found in records. Please insert it into the records"

@tool
def add_new_stock(
    symbol: str,
    company_name: str,
    sector: str
) -> str:
    """Add a new stock to the records if it doesn't exist"""
    return add_stock(symbol, company_name, sector)

@tool
def add_new_record(
    symbol: str,
    transaction_type: str,
    quantity: int,
    price_per_share: float,
    transaction_date: str,
    notes: str = None
) -> str:
    """
    Add a transaction to the records. This is an internal function that should be called
    after verifying the stock exists.
    """
    return add_record(symbol, transaction_type, quantity, price_per_share, transaction_date, notes)

add_transaction_tools = [check_stock_present, add_new_stock, add_new_record]