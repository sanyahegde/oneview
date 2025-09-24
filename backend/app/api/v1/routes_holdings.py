"""Holdings routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.holding import UnifiedHolding
from app.models.user import User
from app.models.holding import Holding
from app.models.account import Account
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=List[UnifiedHolding])
async def get_holdings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[UnifiedHolding]:
    """Get unified holdings across all accounts."""
    # Get all accounts for user
    accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
    account_ids = [account.id for account in accounts]
    
    if not account_ids:
        return []
    
    # Get all holdings for user's accounts
    holdings = db.query(Holding).filter(Holding.account_id.in_(account_ids)).all()
    
    # Create account lookup
    account_lookup = {account.id: account for account in accounts}
    
    # Convert to unified holdings
    unified_holdings = []
    for holding in holdings:
        account = account_lookup[holding.account_id]
        unified_holding = UnifiedHolding(
            symbol=holding.symbol,
            quantity=holding.quantity,
            avg_cost=holding.avg_cost,
            current_price=holding.current_price,
            value=holding.value,
            account_id=holding.account_id,
            account_name=account.name,
            provider=account.provider
        )
        unified_holdings.append(unified_holding)
    
    return unified_holdings
