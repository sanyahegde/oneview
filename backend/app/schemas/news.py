from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NewsArticleResponse(BaseModel):
    id: int
    symbol: str
    title: str
    source: Optional[str] = None
    url: Optional[str] = None
    published_at: datetime
    summary: Optional[str] = None
    sentiment_score: Optional[float] = None
    
    class Config:
        from_attributes = True


class StockSentimentResponse(BaseModel):
    symbol: str
    sentiment_score: float
    sentiment_label: str
    news_count: int
    calculated_at: datetime
    
    class Config:
        from_attributes = True

