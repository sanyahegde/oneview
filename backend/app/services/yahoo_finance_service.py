import httpx
from typing import Optional, Dict
import json


async def get_stock_quote(symbol: str) -> Optional[Dict]:
    """
    Fetch real-time stock data from Yahoo Finance API (using yfinance-like endpoint).
    This uses a public Yahoo Finance API endpoint.
    """
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol.upper()}"
        params = {
            "interval": "1d",
            "range": "1d"
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if "chart" in data and "result" in data["chart"] and len(data["chart"]["result"]) > 0:
                    result = data["chart"]["result"][0]
                    meta = result.get("meta", {})
                    
                    return {
                        "symbol": symbol.upper(),
                        "price": meta.get("regularMarketPrice"),
                        "previous_close": meta.get("previousClose"),
                        "change": meta.get("regularMarketPrice", 0) - meta.get("previousClose", 0),
                        "change_percent": ((meta.get("regularMarketPrice", 0) - meta.get("previousClose", 0)) / meta.get("previousClose", 1)) * 100 if meta.get("previousClose") else 0,
                        "volume": meta.get("regularMarketVolume"),
                        "market_cap": meta.get("marketCap"),
                        "currency": meta.get("currency", "USD")
                    }
    except Exception as e:
        print(f"Error fetching Yahoo Finance data for {symbol}: {e}")
    
    return None


async def get_stock_price(symbol: str) -> Optional[float]:
    """Get current stock price from Yahoo Finance."""
    quote = await get_stock_quote(symbol)
    return quote.get("price") if quote else None


async def get_multiple_stock_quotes(symbols: list) -> Dict[str, Dict]:
    """Fetch quotes for multiple symbols."""
    quotes = {}
    for symbol in symbols:
        quote = await get_stock_quote(symbol)
        if quote:
            quotes[symbol.upper()] = quote
    return quotes

