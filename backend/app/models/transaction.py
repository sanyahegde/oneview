"""Transaction model."""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class TransactionType(str, enum.Enum):
    """Transaction type enumeration."""
    BUY = "buy"
    SELL = "sell"
    DIVIDEND = "dividend"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


class Transaction(Base):
    """Transaction model."""
    
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    symbol = Column(String, nullable=True, index=True)  # None for cash transactions
    type = Column(Enum(TransactionType), nullable=False)
    quantity = Column(Float, nullable=True)  # None for cash transactions
    price = Column(Float, nullable=True)  # None for cash transactions
    amount = Column(Float, nullable=False)  # Total transaction amount
    date = Column(DateTime(timezone=True), nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    account = relationship("Account", back_populates="transactions")
