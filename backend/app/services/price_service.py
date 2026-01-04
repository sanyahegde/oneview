from typing import Dict, Optional
from app.services.yahoo_finance_service import get_stock_price as get_yahoo_price


async def get_stock_price(symbol: str) -> Optional[float]:
    """
    Fetch current stock price from Yahoo Finance API.
    Falls back to mock data if API fails.
    """
    try:
        # Try Yahoo Finance first
        price = await get_yahoo_price(symbol)
        if price:
            return price
    except Exception as e:
        print(f"Error fetching real price for {symbol}: {e}")
    
    # Fallback to mock prices for development
    mock_prices: Dict[str, float] = {
        "AAPL": 175.50,
        "GOOGL": 140.25,
        "MSFT": 380.00,
        "AMZN": 145.75,
        "TSLA": 250.30,
    }
    
    return mock_prices.get(symbol.upper(), 100.0)
