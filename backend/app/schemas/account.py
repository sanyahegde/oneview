"""Account schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.models.account import AccountType


class AccountBase(BaseModel):
    """Base account schema."""
    provider: str
    provider_account_id: str
    account_type: AccountType
    name: Optional[str] = None


class AccountCreate(AccountBase):
    """Account creation schema."""
    public_token: str


class AccountUpdate(BaseModel):
    """Account update schema."""
    name: Optional[str] = None


class AccountInDB(AccountBase):
    """Account in database schema."""
    id: int
    user_id: int
    access_token: Optional[str] = None
    last_sync: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Account(AccountInDB):
    """Account response schema."""
    pass


class AccountLink(BaseModel):
    """Account link request schema."""
    provider: str
    public_token: str


class AccountLinkResponse(BaseModel):
    """Account link response schema."""
    account_id: int
    provider: str
    status: str
