"""Account model."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class AccountType(str, enum.Enum):
    """Account type enumeration."""
    BROKERAGE = "brokerage"
    BANK = "bank"


class Account(Base):
    """Account model."""
    
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(String, nullable=False)  # robinhood, schwab, plaid, akoya
    provider_account_id = Column(String, nullable=False)
    account_type = Column(Enum(AccountType), nullable=False)
    name = Column(String, nullable=True)
    access_token = Column(String, nullable=True)  # Mock token for development
    last_sync = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="accounts")
    holdings = relationship("Holding", back_populates="account", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")
