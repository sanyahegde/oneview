from openai import OpenAI
from typing import List, Dict
from app.core.config import settings


async def analyze_sentiment(headlines: List[str]) -> float:
    """
    Analyze sentiment of financial news headlines using OpenAI.
    Returns a sentiment score between -1 (negative) and 1 (positive).
    """
    if not headlines:
        return 0.0
    
    prompt = f"""Analyze the sentiment of the following financial news headlines about a stock.
    Return a single sentiment score between -1.0 (very negative) and 1.0 (very positive), 
    where 0.0 is neutral. Consider the financial context - positive news includes earnings beats, 
    price increases, favorable analyst ratings. Negative news includes losses, scandals, downgrades.
    
    Headlines:
    {chr(10).join(f"- {headline}" for headline in headlines[:10])}
    
    Respond with only a decimal number between -1.0 and 1.0:"""
    
    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial sentiment analysis expert. Return only a number."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=10
        )
        
        score_str = response.choices[0].message.content.strip()
        score = float(score_str)
        return max(-1.0, min(1.0, score))  # Clamp between -1 and 1
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return 0.0


async def summarize_news(symbol: str, headlines: List[str], articles: List[Dict]) -> str:
    """
    Generate a concise natural-language summary of recent financial news for a stock.
    """
    if not headlines:
        return f"No recent news available for {symbol}."
    
    articles_text = "\n".join([
        f"Title: {art.get('title', '')}\nSource: {art.get('source', 'Unknown')}\n"
        for art in articles[:5]
    ])
    
    prompt = f"""Summarize the recent financial news for {symbol} in 2-3 concise sentences.
    Focus on the most important developments that would be relevant to investors.
    
    Recent headlines and articles:
    {articles_text}
    
    Provide a clear, investor-focused summary:"""
    
    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial news summarizer. Provide concise, investor-focused summaries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=150
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in news summarization: {e}")
        return f"Unable to generate summary for {symbol} due to an error."


def get_sentiment_label(score: float) -> str:
    """Convert sentiment score to label."""
    if score > 0.2:
        return "positive"
    elif score < -0.2:
        return "negative"
    else:
        return "neutral"

