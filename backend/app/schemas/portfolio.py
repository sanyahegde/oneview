from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class HoldingBase(BaseModel):
    symbol: str = Field(..., description="Stock symbol (e.g., AAPL)")
    quantity: float = Field(..., gt=0, description="Number of shares")
    average_cost: float = Field(..., gt=0, description="Average purchase price per share")


class HoldingCreate(HoldingBase):
    pass


class HoldingUpdate(BaseModel):
    quantity: Optional[float] = Field(None, gt=0)
    average_cost: Optional[float] = Field(None, gt=0)
    current_price: Optional[float] = None


class HoldingResponse(HoldingBase):
    id: int
    portfolio_id: int
    current_price: Optional[float] = None
    market_value: Optional[float] = None
    gain_loss: Optional[float] = None
    gain_loss_percent: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class PortfolioCreate(BaseModel):
    name: str = Field(default="My Portfolio", description="Portfolio name")


class PortfolioResponse(BaseModel):
    id: int
    user_id: int
    name: str
    holdings: List[HoldingResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PortfolioSummary(BaseModel):
    portfolio_id: int
    portfolio_name: str
    total_holdings: int
    total_cost_basis: float
    total_market_value: float
    total_gain_loss: float
    total_gain_loss_percent: float
    asset_allocation: List[dict]  # [{symbol: str, allocation: float, value: float}]
    holdings: List[HoldingResponse]


class PortfolioSnapshotResponse(BaseModel):
    id: int
    portfolio_id: int
    total_value: float
    total_cost_basis: float
    total_gain_loss: float
    total_gain_loss_percent: float
    snapshot_date: datetime
    
    class Config:
        from_attributes = True


class HistoricalPerformance(BaseModel):
    portfolio_id: int
    portfolio_name: str
    data_points: List[PortfolioSnapshotResponse]
    current_value: float
    initial_value: Optional[float] = None
    total_return: Optional[float] = None
    total_return_percent: Optional[float] = None

