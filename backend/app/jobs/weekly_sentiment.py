"""Weekly sentiment analysis job."""

import asyncio
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.holding import Holding


class SentimentScore:
    """Sentiment score model."""
    
    def __init__(self, symbol: str, score: float, headlines: list):
        self.symbol = symbol
        self.score = score  # -1 to 1, where 1 is very positive
        self.headlines = headlines


async def run_weekly_sentiment() -> None:
    """Run weekly sentiment analysis for all holdings."""
    db = next(get_db())
    
    try:
        # Get all unique symbols from holdings
        holdings = db.query(Holding).all()
        symbols = list(set([holding.symbol for holding in holdings]))
        
        print(f"Running sentiment analysis for {len(symbols)} symbols")
        
        for symbol in symbols:
            try:
                # Mock sentiment analysis
                # In production, this would use the ML model
                sentiment_score = analyze_sentiment(symbol)
                
                print(f"Symbol: {symbol}, Sentiment: {sentiment_score.score:.2f}")
                
                # In production, save to sentiment_scores table
                # For now, just log the results
                
            except Exception as e:
                print(f"Error analyzing sentiment for {symbol}: {e}")
        
        print("Completed weekly sentiment analysis")
        
    except Exception as e:
        print(f"Error in weekly sentiment job: {e}")
    finally:
        db.close()


def analyze_sentiment(symbol: str) -> SentimentScore:
    """Analyze sentiment for a symbol (mock implementation)."""
    # Mock headlines
    headlines = [
        f"{symbol} reports strong quarterly earnings",
        f"Analysts upgrade {symbol} to buy rating",
        f"{symbol} faces regulatory challenges",
        f"Market volatility impacts {symbol} performance",
        f"{symbol} announces new product launch"
    ]
    
    # Mock sentiment scores for headlines
    headline_scores = [
        {"title": headline, "score": random.uniform(-0.5, 0.8)}
        for headline in headlines
    ]
    
    # Calculate average sentiment
    avg_sentiment = sum(h["score"] for h in headline_scores) / len(headline_scores)
    
    return SentimentScore(symbol, avg_sentiment, headline_scores)


if __name__ == "__main__":
    asyncio.run(run_weekly_sentiment())
