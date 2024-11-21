# src/database/models.py

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Stock:
    stock_id: int
    symbol: str
    company_name: str
    sector: str

@dataclass
class Transaction:
    transaction_id: int
    stock_id: int
    transaction_type: str
    quantity: int
    price_per_share: float
    transaction_date: datetime
    total_amount: float
    notes: str
    created_at: datetime