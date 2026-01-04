from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.models.portfolio import Portfolio
from app.services.chatbot_service import get_portfolio_insights, chat_with_portfolio
from app.api.v1.endpoints.portfolios import CURRENT_USER_ID
from app.schemas.portfolio import PortfolioSummary

# Import the function properly
async def get_portfolio_summary_internal(portfolio_id: int, db: Session) -> PortfolioSummary:
    """Helper to get portfolio summary for chatbot."""
    from app.api.v1.endpoints.portfolios import get_portfolio_summary
    return await get_portfolio_summary(portfolio_id, db)

router = APIRouter()


class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@router.get("/portfolio/{portfolio_id}/insights", response_model=ChatResponse)
async def get_insights(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    """Get AI-generated insights about the portfolio."""
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == CURRENT_USER_ID
    ).first()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Get portfolio summary
    summary = await get_portfolio_summary_internal(portfolio_id, db)
    
    # Convert to dict for the service
    holdings_data = [
        {
            "symbol": h.symbol,
            "quantity": h.quantity,
            "average_cost": h.average_cost,
            "current_price": h.current_price,
            "market_value": h.quantity * (h.current_price or h.average_cost),
            "gain_loss": (h.quantity * (h.current_price or h.average_cost)) - (h.quantity * h.average_cost),
            "gain_loss_percent": (((h.quantity * (h.current_price or h.average_cost)) - (h.quantity * h.average_cost)) / (h.quantity * h.average_cost) * 100) if h.quantity * h.average_cost > 0 else 0
        }
        for h in summary.holdings
    ]
    
    summary_data = {
        "total_market_value": summary.total_market_value,
        "total_cost_basis": summary.total_cost_basis,
        "total_gain_loss": summary.total_gain_loss,
        "total_gain_loss_percent": summary.total_gain_loss_percent,
        "total_holdings": summary.total_holdings
    }
    
    insights = await get_portfolio_insights(summary_data, holdings_data)
    
    return ChatResponse(response=insights)


@router.post("/portfolio/{portfolio_id}/chat", response_model=ChatResponse)
async def chat(
    portfolio_id: int,
    message: ChatMessage,
    db: Session = Depends(get_db)
):
    """Chat with AI about the portfolio."""
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == CURRENT_USER_ID
    ).first()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Get portfolio summary
    summary = await get_portfolio_summary_internal(portfolio_id, db)
    
    # Convert to dict for the service
    holdings_data = [
        {
            "symbol": h.symbol,
            "quantity": h.quantity,
            "average_cost": h.average_cost,
            "current_price": h.current_price,
            "market_value": h.quantity * (h.current_price or h.average_cost),
        }
        for h in summary.holdings
    ]
    
    summary_data = {
        "total_market_value": summary.total_market_value,
        "total_cost_basis": summary.total_cost_basis,
        "total_gain_loss": summary.total_gain_loss,
        "total_gain_loss_percent": summary.total_gain_loss_percent,
        "total_holdings": summary.total_holdings
    }
    
    response = await chat_with_portfolio(message.message, summary_data, holdings_data)
    
    return ChatResponse(response=response)

