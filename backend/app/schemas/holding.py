"""Holding schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class HoldingBase(BaseModel):
    """Base holding schema."""
    symbol: str
    quantity: float
    avg_cost: float
    current_price: float
    value: float


class HoldingCreate(HoldingBase):
    """Holding creation schema."""
    account_id: int


class HoldingUpdate(BaseModel):
    """Holding update schema."""
    quantity: Optional[float] = None
    avg_cost: Optional[float] = None
    current_price: Optional[float] = None
    value: Optional[float] = None


class HoldingInDB(HoldingBase):
    """Holding in database schema."""
    id: int
    account_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Holding(HoldingInDB):
    """Holding response schema."""
    pass


class UnifiedHolding(BaseModel):
    """Unified holding schema for API response."""
    symbol: str
    quantity: float
    avg_cost: float
    current_price: float
    value: float
    account_id: int
    account_name: Optional[str] = None
    provider: Optional[str] = None
