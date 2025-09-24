"""Account routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.account import Account, AccountLink, AccountLinkResponse
from app.models.account import Account as AccountModel
from app.models.user import User
from app.api.deps import get_current_user
from app.services.aggregators.mock_broker import MockBrokerAggregator
from app.services.aggregators.mock_bank import MockBankAggregator

router = APIRouter()


@router.post("/link", response_model=AccountLinkResponse)
async def link_account(
    account_link: AccountLink,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> AccountLinkResponse:
    """Link an external account."""
    # Determine account type based on provider
    if account_link.provider in ["robinhood", "schwab"]:
        account_type = "brokerage"
        aggregator = MockBrokerAggregator()
    elif account_link.provider in ["plaid", "akoya"]:
        account_type = "bank"
        aggregator = MockBankAggregator()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported provider"
        )
    
    # Exchange public token for access token
    try:
        access_token = aggregator.exchange_token(account_link.public_token)
        account_info = aggregator.get_account_info(access_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to link account: {str(e)}"
        )
    
    # Create account record
    account = AccountModel(
        user_id=current_user.id,
        provider=account_link.provider,
        provider_account_id=account_info["account_id"],
        account_type=account_type,
        name=account_info.get("name"),
        access_token=access_token
    )
    
    db.add(account)
    db.commit()
    db.refresh(account)
    
    return AccountLinkResponse(
        account_id=account.id,
        provider=account.provider,
        status="linked"
    )


@router.get("/", response_model=List[Account])
async def get_accounts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[AccountModel]:
    """Get all linked accounts for current user."""
    accounts = db.query(AccountModel).filter(AccountModel.user_id == current_user.id).all()
    return accounts


@router.get("/{account_id}", response_model=Account)
async def get_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> AccountModel:
    """Get specific account by ID."""
    account = db.query(AccountModel).filter(
        AccountModel.id == account_id,
        AccountModel.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    return account
