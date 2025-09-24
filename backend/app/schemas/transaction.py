"""Transaction schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.models.transaction import TransactionType


class TransactionBase(BaseModel):
    """Base transaction schema."""
    symbol: Optional[str] = None
    type: TransactionType
    quantity: Optional[float] = None
    price: Optional[float] = None
    amount: float
    date: datetime
    description: Optional[str] = None


class TransactionCreate(TransactionBase):
    """Transaction creation schema."""
    account_id: int


class TransactionUpdate(BaseModel):
    """Transaction update schema."""
    symbol: Optional[str] = None
    type: Optional[TransactionType] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    amount: Optional[float] = None
    date: Optional[datetime] = None
    description: Optional[str] = None


class TransactionInDB(TransactionBase):
    """Transaction in database schema."""
    id: int
    account_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class Transaction(TransactionInDB):
    """Transaction response schema."""
    pass


class TransactionFilters(BaseModel):
    """Transaction filters schema."""
    symbol: Optional[str] = None
    type: Optional[TransactionType] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    page: int = 1
    page_size: int = 50


class PaginatedTransactions(BaseModel):
    """Paginated transactions response schema."""
    items: list[Transaction]
    total: int
    page: int
    page_size: int
    pages: int
