from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from app.core.database import get_db
from app.schemas.news import NewsArticleResponse, StockSentimentResponse
from app.models.news import NewsArticle, StockSentiment
from app.models.portfolio import Holding
from app.services.news_service import fetch_financial_news
from app.services.openai_service import analyze_sentiment, summarize_news, get_sentiment_label

router = APIRouter()

# Temporary user ID for development
CURRENT_USER_ID = 1


@router.get("/symbol/{symbol}", response_model=List[NewsArticleResponse])
async def get_news_for_symbol(
    symbol: str,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """Get news articles for a specific stock symbol with sentiment analysis and summaries."""
    # Check if we have recent articles in the database (within last 24 hours)
    from datetime import timedelta
    recent_cutoff = datetime.utcnow() - timedelta(hours=24)
    existing_articles = db.query(NewsArticle).filter(
        NewsArticle.symbol == symbol.upper(),
        NewsArticle.published_at >= recent_cutoff
    ).order_by(NewsArticle.published_at.desc()).limit(limit).all()
    
    if existing_articles and len(existing_articles) >= limit:
        # Return existing articles with summaries
        return [NewsArticleResponse(
            id=art.id,
            symbol=art.symbol,
            title=art.title,
            source=art.source,
            url=art.url,
            published_at=art.published_at,
            summary=art.summary,
            sentiment_score=art.sentiment_score
        ) for art in existing_articles[:limit]]
    
    # Fetch news from external API
    news_data = await fetch_financial_news(symbol.upper(), limit)
    
    # Store in database
    articles = []
    for news_item in news_data:
        db_article = NewsArticle(
            symbol=symbol.upper(),
            title=news_item["title"],
            source=news_item.get("source"),
            url=news_item.get("url"),
            published_at=news_item["published_at"],
            raw_content=news_item.get("content")
        )
        db.add(db_article)
        articles.append(db_article)
    
    db.commit()
    
    # Analyze sentiment and generate summaries
    if articles:
        headlines = [art.title for art in articles]
        sentiment_score = await analyze_sentiment(headlines)
        summary = await summarize_news(symbol.upper(), headlines, news_data)
        
        # Update articles with sentiment and summary
        for article in articles:
            article.sentiment_score = sentiment_score
            article.summary = summary
            db.add(article)
        
        db.commit()
    
    return [NewsArticleResponse(
        id=art.id,
        symbol=art.symbol,
        title=art.title,
        source=art.source,
        url=art.url,
        published_at=art.published_at,
        summary=art.summary,
        sentiment_score=art.sentiment_score
    ) for art in articles]


@router.get("/sentiment/{symbol}", response_model=StockSentimentResponse)
async def get_sentiment_for_symbol(
    symbol: str,
    db: Session = Depends(get_db)
):
    """Get sentiment analysis for a specific stock symbol."""
    # Get recent news articles
    recent_articles = db.query(NewsArticle).filter(
        NewsArticle.symbol == symbol.upper(),
        NewsArticle.published_at >= datetime.utcnow() - timedelta(days=7)
    ).all()
    
    if not recent_articles:
        # Fetch new news if none exists
        news_data = await fetch_financial_news(symbol.upper(), 10)
        headlines = [item["title"] for item in news_data]
        sentiment_score = await analyze_sentiment(headlines)
    else:
        # Calculate average sentiment from existing articles
        scores = [art.sentiment_score for art in recent_articles if art.sentiment_score is not None]
        sentiment_score = sum(scores) / len(scores) if scores else 0.0
    
    sentiment_label = get_sentiment_label(sentiment_score)
    
    # Update or create sentiment record
    sentiment = db.query(StockSentiment).filter(
        StockSentiment.symbol == symbol.upper()
    ).first()
    
    if sentiment:
        sentiment.sentiment_score = sentiment_score
        sentiment.sentiment_label = sentiment_label
        sentiment.news_count = len(recent_articles)
        sentiment.updated_at = datetime.utcnow()
    else:
        sentiment = StockSentiment(
            symbol=symbol.upper(),
            sentiment_score=sentiment_score,
            sentiment_label=sentiment_label,
            news_count=len(recent_articles)
        )
        db.add(sentiment)
    
    db.commit()
    db.refresh(sentiment)
    
    return StockSentimentResponse(
        symbol=sentiment.symbol,
        sentiment_score=sentiment.sentiment_score,
        sentiment_label=sentiment.sentiment_label,
        news_count=sentiment.news_count,
        calculated_at=sentiment.calculated_at
    )


@router.get("/portfolio/{portfolio_id}/sentiments", response_model=List[StockSentimentResponse])
async def get_portfolio_sentiments(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    """Get sentiment analysis for all stocks in a portfolio."""
    from app.models.portfolio import Portfolio
    
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == CURRENT_USER_ID
    ).first()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Get unique symbols from holdings
    symbols = set([holding.symbol for holding in portfolio.holdings])
    
    sentiments = []
    for symbol in symbols:
        sentiment = await get_sentiment_for_symbol(symbol, db)
        sentiments.append(sentiment)
    
    return sentiments

