"""Transaction routes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from typing import List, Optional

from app.db.session import get_db
from app.schemas.transaction import Transaction, TransactionFilters, PaginatedTransactions
from app.models.user import User
from app.models.transaction import Transaction as TransactionModel, TransactionType
from app.models.account import Account
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=PaginatedTransactions)
async def get_transactions(
    symbol: Optional[str] = Query(None),
    type: Optional[TransactionType] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> PaginatedTransactions:
    """Get transactions with filters and pagination."""
    # Get all accounts for user
    accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
    account_ids = [account.id for account in accounts]
    
    if not account_ids:
        return PaginatedTransactions(
            items=[],
            total=0,
            page=page,
            page_size=page_size,
            pages=0
        )
    
    # Build query
    query = db.query(TransactionModel).filter(TransactionModel.account_id.in_(account_ids))
    
    # Apply filters
    if symbol:
        query = query.filter(TransactionModel.symbol.ilike(f"%{symbol}%"))
    
    if type:
        query = query.filter(TransactionModel.type == type)
    
    if date_from:
        query = query.filter(TransactionModel.date >= date_from)
    
    if date_to:
        query = query.filter(TransactionModel.date <= date_to)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    transactions = query.order_by(TransactionModel.date.desc()).offset(offset).limit(page_size).all()
    
    # Calculate pages
    pages = (total + page_size - 1) // page_size
    
    return PaginatedTransactions(
        items=transactions,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages
    )
