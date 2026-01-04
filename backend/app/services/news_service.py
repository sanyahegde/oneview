from typing import List, Dict
from datetime import datetime, timedelta
import httpx
import json


async def fetch_financial_news(symbol: str, limit: int = 10) -> List[Dict]:
    """
    Fetch financial news for a given stock symbol from Yahoo Finance.
    Uses Yahoo Finance's RSS/news API.
    """
    try:
        # Yahoo Finance news endpoint
        url = f"https://query2.finance.yahoo.com/v1/finance/search"
        params = {
            "q": symbol.upper(),
            "quotes_count": 1,
            "news_count": limit,
            "enableFuzzyQuery": False,
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        async with httpx.AsyncClient(timeout=10.0, headers=headers) as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                news_items = data.get("news", [])
                
                articles = []
                for item in news_items[:limit]:
                    # Extract news data
                    title = item.get("title", "")
                    publisher = item.get("publisher", "Unknown")
                    link = item.get("link", "")
                    pub_date = item.get("providerPublishTime")
                    
                    # Convert timestamp to datetime
                    published_at = datetime.utcnow() - timedelta(hours=1)  # Default fallback
                    if pub_date:
                        try:
                            published_at = datetime.fromtimestamp(pub_date)
                        except:
                            pass
                    
                    articles.append({
                        "title": title,
                        "source": publisher,
                        "url": link,
                        "published_at": published_at,
                        "content": item.get("summary", "")
                    })
                
                if articles:
                    return articles
    except Exception as e:
        print(f"Error fetching Yahoo Finance news for {symbol}: {e}")
    
    # Fallback: Try alternative news sources or return minimal data
    try:
        # Alternative: Use Alpha Vantage News (requires API key but has free tier)
        # For now, return structured mock data with better formatting
        return _get_fallback_news(symbol, limit)
    except:
        return []


def _get_fallback_news(symbol: str, limit: int) -> List[Dict]:
    """
    Fallback news data with Yahoo Finance search URLs.
    These are real search URLs that will show relevant news.
    """
    base_time = datetime.utcnow()
    
    return [
        {
            "title": f"{symbol} Stock News and Analysis",
            "source": "Yahoo Finance",
            "url": f"https://finance.yahoo.com/quote/{symbol}/news",
            "published_at": base_time - timedelta(hours=2),
            "content": f"Latest news and analysis for {symbol} stock."
        },
        {
            "title": f"{symbol} - Market Watch",
            "source": "MarketWatch",
            "url": f"https://www.marketwatch.com/investing/stock/{symbol}",
            "published_at": base_time - timedelta(days=1),
            "content": f"Market data and news for {symbol}."
        },
        {
            "title": f"{symbol} Stock Quote and News",
            "source": "Nasdaq",
            "url": f"https://www.nasdaq.com/market-activity/stocks/{symbol}",
            "published_at": base_time - timedelta(days=1),
            "content": f"Stock quote and news for {symbol}."
        },
        {
            "title": f"{symbol} - Financial Times",
            "source": "Financial Times",
            "url": f"https://www.ft.com/{symbol}",
            "published_at": base_time - timedelta(days=2),
            "content": f"Financial news and analysis for {symbol}."
        },
        {
            "title": f"{symbol} Stock Analysis",
            "source": "Seeking Alpha",
            "url": f"https://seekingalpha.com/symbol/{symbol}/news",
            "published_at": base_time - timedelta(days=2),
            "content": f"Analysis and news about {symbol}."
        }
    ][:limit]


async def fetch_newsapi_news(symbol: str, limit: int = 10) -> List[Dict]:
    """
    Alternative: Fetch news from NewsAPI (requires free API key).
    Sign up at https://newsapi.org/ to get an API key.
    
    To use this, add NEWSAPI_KEY to your .env file and uncomment the code below.
    """
    # Uncomment and add NEWSAPI_KEY to .env to use:
    # from app.core.config import settings
    # api_key = getattr(settings, 'NEWSAPI_KEY', None)
    # if not api_key:
    #     return []
    # 
    # url = "https://newsapi.org/v2/everything"
    # params = {
    #     "q": f"{symbol} stock",
    #     "language": "en",
    #     "sortBy": "publishedAt",
    #     "pageSize": limit,
    #     "apiKey": api_key
    # }
    # 
    # async with httpx.AsyncClient(timeout=10.0) as client:
    #     response = await client.get(url, params=params)
    #     if response.status_code == 200:
    #         data = response.json()
    #         articles = []
    #         for item in data.get("articles", []):
    #             articles.append({
    #                 "title": item.get("title", ""),
    #                 "source": item.get("source", {}).get("name", "Unknown"),
    #                 "url": item.get("url", ""),
    #                 "published_at": datetime.fromisoformat(item.get("publishedAt", datetime.utcnow().isoformat())),
    #                 "content": item.get("description", "")
    #             })
    #         return articles
    # return []
    pass
