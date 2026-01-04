from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime, timedelta
from app.core.database import get_db
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioResponse,
    HoldingCreate,
    HoldingUpdate,
    HoldingResponse,
    PortfolioSummary,
    HistoricalPerformance,
    PortfolioSnapshotResponse
)
from app.models.portfolio import Portfolio, Holding
from app.models.portfolio_snapshot import PortfolioSnapshot
from app.services.price_service import get_stock_price

router = APIRouter()


# Temporary user ID for development (replace with auth later)
CURRENT_USER_ID = 1


@router.get("/", response_model=List[PortfolioResponse])
async def get_portfolios(db: Session = Depends(get_db)):
    """Get all portfolios for the current user."""
    portfolios = db.query(Portfolio).filter(Portfolio.user_id == CURRENT_USER_ID).all()
    return portfolios


@router.post("/", response_model=PortfolioResponse, status_code=201)
async def create_portfolio(
    portfolio: PortfolioCreate,
    db: Session = Depends(get_db)
):
    """Create a new portfolio."""
    db_portfolio = Portfolio(
        user_id=CURRENT_USER_ID,
        name=portfolio.name
    )
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio


@router.get("/{portfolio_id}", response_model=PortfolioResponse)
async def get_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    """Get a specific portfolio by ID."""
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == CURRENT_USER_ID
    ).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio


@router.get("/{portfolio_id}/summary", response_model=PortfolioSummary)
async def get_portfolio_summary(portfolio_id: int, db: Session = Depends(get_db)):
    """Get portfolio summary with calculated values."""
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == CURRENT_USER_ID
    ).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Update current prices
    holdings_with_prices = []
    total_cost_basis = 0.0
    total_market_value = 0.0
    
    for holding in portfolio.holdings:
        current_price = await get_stock_price(holding.symbol)
        if current_price:
            holding.current_price = current_price
        
        cost_basis = holding.quantity * holding.average_cost
        market_value = holding.quantity * (holding.current_price or holding.average_cost)
        gain_loss = market_value - cost_basis
        gain_loss_percent = (gain_loss / cost_basis * 100) if cost_basis > 0 else 0
        
        total_cost_basis += cost_basis
        total_market_value += market_value
        
        holdings_with_prices.append(HoldingResponse(
            id=holding.id,
            portfolio_id=holding.portfolio_id,
            symbol=holding.symbol,
            quantity=holding.quantity,
            average_cost=holding.average_cost,
            current_price=holding.current_price,
            market_value=market_value,
            gain_loss=gain_loss,
            gain_loss_percent=gain_loss_percent,
            created_at=holding.created_at
        ))
    
    db.commit()
    
    total_gain_loss = total_market_value - total_cost_basis
    total_gain_loss_percent = (total_gain_loss / total_cost_basis * 100) if total_cost_basis > 0 else 0
    
    # Calculate asset allocation
    asset_allocation = []
    for holding in holdings_with_prices:
        if holding.market_value and total_market_value > 0:
            allocation = (holding.market_value / total_market_value) * 100
            asset_allocation.append({
                "symbol": holding.symbol,
                "allocation": round(allocation, 2),
                "value": holding.market_value
            })
    
    # Create snapshot for historical tracking
    snapshot = PortfolioSnapshot(
        portfolio_id=portfolio.id,
        total_value=round(total_market_value, 2),
        total_cost_basis=round(total_cost_basis, 2),
        total_gain_loss=round(total_gain_loss, 2),
        total_gain_loss_percent=round(total_gain_loss_percent, 2)
    )
    db.add(snapshot)
    db.commit()
    
    return PortfolioSummary(
        portfolio_id=portfolio.id,
        portfolio_name=portfolio.name,
        total_holdings=len(holdings_with_prices),
        total_cost_basis=round(total_cost_basis, 2),
        total_market_value=round(total_market_value, 2),
        total_gain_loss=round(total_gain_loss, 2),
        total_gain_loss_percent=round(total_gain_loss_percent, 2),
        asset_allocation=asset_allocation,
        holdings=holdings_with_prices
    )


@router.post("/{portfolio_id}/holdings", response_model=HoldingResponse, status_code=201)
async def add_holding(
    portfolio_id: int,
    holding: HoldingCreate,
    db: Session = Depends(get_db)
):
    """Add a holding to a portfolio."""
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == CURRENT_USER_ID
    ).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    current_price = await get_stock_price(holding.symbol)
    
    db_holding = Holding(
        portfolio_id=portfolio_id,
        symbol=holding.symbol.upper(),
        quantity=holding.quantity,
        average_cost=holding.average_cost,
        current_price=current_price
    )
    db.add(db_holding)
    db.commit()
    db.refresh(db_holding)
    
    return HoldingResponse(
        id=db_holding.id,
        portfolio_id=db_holding.portfolio_id,
        symbol=db_holding.symbol,
        quantity=db_holding.quantity,
        average_cost=db_holding.average_cost,
        current_price=db_holding.current_price,
        market_value=db_holding.quantity * (db_holding.current_price or db_holding.average_cost),
        gain_loss=None,
        gain_loss_percent=None,
        created_at=db_holding.created_at
    )


@router.put("/{portfolio_id}/holdings/{holding_id}", response_model=HoldingResponse)
async def update_holding(
    portfolio_id: int,
    holding_id: int,
    holding_update: HoldingUpdate,
    db: Session = Depends(get_db)
):
    """Update a holding in a portfolio."""
    holding = db.query(Holding).filter(
        Holding.id == holding_id,
        Holding.portfolio_id == portfolio_id
    ).first()
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    
    if holding_update.quantity is not None:
        holding.quantity = holding_update.quantity
    if holding_update.average_cost is not None:
        holding.average_cost = holding_update.average_cost
    if holding_update.current_price is not None:
        holding.current_price = holding_update.current_price
    else:
        # Fetch latest price if not provided
        holding.current_price = await get_stock_price(holding.symbol)
    
    db.commit()
    db.refresh(holding)
    
    market_value = holding.quantity * (holding.current_price or holding.average_cost)
    cost_basis = holding.quantity * holding.average_cost
    gain_loss = market_value - cost_basis
    gain_loss_percent = (gain_loss / cost_basis * 100) if cost_basis > 0 else 0
    
    return HoldingResponse(
        id=holding.id,
        portfolio_id=holding.portfolio_id,
        symbol=holding.symbol,
        quantity=holding.quantity,
        average_cost=holding.average_cost,
        current_price=holding.current_price,
        market_value=market_value,
        gain_loss=gain_loss,
        gain_loss_percent=gain_loss_percent,
        created_at=holding.created_at
    )


@router.delete("/{portfolio_id}/holdings/{holding_id}", status_code=204)
async def delete_holding(
    portfolio_id: int,
    holding_id: int,
    db: Session = Depends(get_db)
):
    """Delete a holding from a portfolio."""
    holding = db.query(Holding).filter(
        Holding.id == holding_id,
        Holding.portfolio_id == portfolio_id
    ).first()
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    
    db.delete(holding)
    db.commit()
    return None


@router.get("/{portfolio_id}/performance", response_model=HistoricalPerformance)
async def get_historical_performance(
    portfolio_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get historical performance data for a portfolio."""
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == CURRENT_USER_ID
    ).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Get snapshots from the last N days
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    snapshots = db.query(PortfolioSnapshot).filter(
        PortfolioSnapshot.portfolio_id == portfolio_id,
        PortfolioSnapshot.snapshot_date >= cutoff_date
    ).order_by(PortfolioSnapshot.snapshot_date.asc()).all()
    
    # Get current portfolio value
    current_summary = await get_portfolio_summary(portfolio_id, db)
    current_value = current_summary.total_market_value
    
    # Calculate total return if we have initial value
    initial_value = None
    total_return = None
    total_return_percent = None
    if snapshots:
        initial_value = snapshots[0].total_value
        total_return = current_value - initial_value
        total_return_percent = (total_return / initial_value * 100) if initial_value > 0 else 0
    
    return HistoricalPerformance(
        portfolio_id=portfolio.id,
        portfolio_name=portfolio.name,
        data_points=[PortfolioSnapshotResponse(
            id=s.id,
            portfolio_id=s.portfolio_id,
            total_value=s.total_value,
            total_cost_basis=s.total_cost_basis,
            total_gain_loss=s.total_gain_loss,
            total_gain_loss_percent=s.total_gain_loss_percent,
            snapshot_date=s.snapshot_date
        ) for s in snapshots],
        current_value=current_value,
        initial_value=initial_value,
        total_return=total_return,
        total_return_percent=total_return_percent
    )

