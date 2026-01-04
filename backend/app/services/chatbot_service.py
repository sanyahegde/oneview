from openai import OpenAI
from typing import List, Dict
from app.core.config import settings
from app.services.yahoo_finance_service import get_multiple_stock_quotes


async def get_portfolio_insights(portfolio_summary: Dict, holdings: List[Dict]) -> str:
    """
    Generate AI insights about the portfolio using OpenAI.
    """
    if not holdings or len(holdings) == 0:
        return "Your portfolio is currently empty. Add some stocks to get started! I can help you analyze your investments once you have some holdings."
    
    # Get real-time stock data
    symbols = [h.get("symbol") for h in holdings]
    stock_quotes = await get_multiple_stock_quotes(symbols)
    
    # Build portfolio summary for LLM
    portfolio_info = f"""
Portfolio Summary:
- Total Value: ${portfolio_summary.get('total_market_value', 0):,.2f}
- Total Cost Basis: ${portfolio_summary.get('total_cost_basis', 0):,.2f}
- Total Gain/Loss: ${portfolio_summary.get('total_gain_loss', 0):,.2f} ({portfolio_summary.get('total_gain_loss_percent', 0):.2f}%)
- Number of Holdings: {portfolio_summary.get('total_holdings', 0)}

Current Holdings:
"""
    
    for holding in holdings:
        symbol = holding.get("symbol")
        quote = stock_quotes.get(symbol, {})
        portfolio_info += f"""
- {symbol}: {holding.get('quantity', 0):.2f} shares
  Cost Basis: ${holding.get('average_cost', 0):.2f}/share
  Current Price: ${quote.get('price', holding.get('current_price', 0)):.2f}/share
  Market Value: ${holding.get('market_value', 0):,.2f}
  Gain/Loss: ${holding.get('gain_loss', 0):,.2f} ({holding.get('gain_loss_percent', 0):.2f}%)
"""
    
    prompt = f"""You are a helpful financial advisor AI assistant. Analyze this portfolio and provide:
1. A brief overview of the portfolio's current state
2. Key insights about performance
3. Risk assessment (if applicable)
4. Any recommendations or observations

Keep the response concise, friendly, and actionable (2-3 paragraphs max).

{portfolio_info}

Provide your analysis:"""

    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful financial advisor AI. Provide clear, concise, and actionable portfolio analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating insights: {e}")
        return "I'm having trouble analyzing your portfolio right now. Please try again later."


async def chat_with_portfolio(user_message: str, portfolio_summary: Dict, holdings: List[Dict]) -> str:
    """
    Chat with the AI about the portfolio. Can answer questions about holdings, performance, etc.
    """
    if not holdings or len(holdings) == 0:
        return "Your portfolio is empty. Add some stocks first, then I can help you analyze them!"
    
    # Get real-time stock data
    symbols = [h.get("symbol") for h in holdings]
    stock_quotes = await get_multiple_stock_quotes(symbols)
    
    # Build context
    context = f"""
Portfolio Context:
- Total Value: ${portfolio_summary.get('total_market_value', 0):,.2f}
- Total Gain/Loss: ${portfolio_summary.get('total_gain_loss', 0):,.2f} ({portfolio_summary.get('total_gain_loss_percent', 0):.2f}%)
- Holdings: {', '.join(symbols)}

Current Stock Prices:
"""
    for symbol, quote in stock_quotes.items():
        context += f"- {symbol}: ${quote.get('price', 0):.2f} ({quote.get('change_percent', 0):.2f}%)\n"
    
    prompt = f"""You are a helpful financial advisor AI assistant. The user is asking about their investment portfolio.

{context}

User Question: {user_message}

Provide a helpful, concise answer (2-3 sentences max). If they ask about specific stocks, use the data above."""

    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful financial advisor AI. Answer questions about the user's portfolio clearly and concisely."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in chatbot: {e}")
        return "I'm having trouble processing your question right now. Please try again later."

