from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.core.database import get_db
from app.services.plaid_service import (
    create_link_token,
    exchange_public_token,
    get_accounts,
    get_transactions,
    get_investment_holdings,
    get_investment_transactions
)

router = APIRouter()


# Temporary user ID for development (replace with auth later)
CURRENT_USER_ID = 1


class PublicTokenRequest(BaseModel):
    public_token: str


class AccessTokenRequest(BaseModel):
    access_token: str


class DateRangeRequest(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None


@router.post("/link/token")
async def create_link_token_endpoint(db: Session = Depends(get_db)):
    """
    Create a Plaid Link token for frontend initialization.
    This token is used to launch Plaid Link in the frontend.
    """
    try:
        result = await create_link_token(CURRENT_USER_ID)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create Link token: {str(e)}")


@router.post("/link/token/exchange")
async def exchange_public_token_endpoint(
    request: PublicTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Exchange a public token from Plaid Link for an access token.
    Store the access_token securely (in database) for future API calls.
    """
    try:
        result = await exchange_public_token(request.public_token)
        # TODO: Store access_token and item_id in database for the user
        # For now, we just return it. You should store it in a PlaidItem model.
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to exchange token: {str(e)}")


@router.post("/accounts")
async def get_accounts_endpoint(
    request: AccessTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Get all accounts (banking and investment) for a Plaid access token.
    """
    try:
        accounts = await get_accounts(request.access_token)
        return {"accounts": accounts}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch accounts: {str(e)}")


@router.post("/transactions")
async def get_transactions_endpoint(
    request: AccessTokenRequest,
    date_range: Optional[DateRangeRequest] = None,
    db: Session = Depends(get_db)
):
    """
    Get transactions for a Plaid access token.
    Optional date range (defaults to last 30 days).
    """
    try:
        start_date = None
        end_date = None
        if date_range:
            if date_range.start_date:
                start_date = datetime.fromisoformat(date_range.start_date.replace('Z', '+00:00'))
            if date_range.end_date:
                end_date = datetime.fromisoformat(date_range.end_date.replace('Z', '+00:00'))
        
        transactions = await get_transactions(request.access_token, start_date, end_date)
        return {"transactions": transactions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch transactions: {str(e)}")


@router.post("/investments/holdings")
async def get_investment_holdings_endpoint(
    request: AccessTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Get investment holdings (securities/stocks) for a Plaid access token.
    """
    try:
        holdings = await get_investment_holdings(request.access_token)
        return {"holdings": holdings}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch investment holdings: {str(e)}")


@router.post("/investments/transactions")
async def get_investment_transactions_endpoint(
    request: AccessTokenRequest,
    date_range: Optional[DateRangeRequest] = None,
    db: Session = Depends(get_db)
):
    """
    Get investment transactions for a Plaid access token.
    Optional date range (defaults to last 30 days).
    """
    try:
        start_date = None
        end_date = None
        if date_range:
            if date_range.start_date:
                start_date = datetime.fromisoformat(date_range.start_date.replace('Z', '+00:00'))
            if date_range.end_date:
                end_date = datetime.fromisoformat(date_range.end_date.replace('Z', '+00:00'))
        
        transactions = await get_investment_transactions(request.access_token, start_date, end_date)
        return {"transactions": transactions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch investment transactions: {str(e)}")

