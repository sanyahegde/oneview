"""Database initialization and seeding."""

from sqlalchemy.orm import Session
from app.db.base import engine, Base
from app.models.user import User
from app.models.account import Account
from app.models.holding import Holding
from app.models.transaction import Transaction
from app.core.security import get_password_hash
from datetime import datetime, timedelta
import random


async def init_db() -> None:
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
    await seed_demo_data()


async def seed_demo_data() -> None:
    """Seed database with demo data."""
    from app.db.session import get_db
    
    db = next(get_db())
    
    # Check if demo user already exists
    existing_user = db.query(User).filter(User.email == "demo@portfolioai.com").first()
    if existing_user:
        return
    
    # Create demo user
    demo_user = User(
        email="demo@portfolioai.com",
        hashed_password=get_password_hash("demo123"),
        full_name="Demo User",
        is_active=True
    )
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)
    
    # Create demo accounts
    accounts_data = [
        {
            "provider": "robinhood",
            "provider_account_id": "rh_demo_001",
            "account_type": "brokerage",
            "name": "Robinhood Demo Account",
            "access_token": "mock_rh_token_001"
        },
        {
            "provider": "schwab",
            "provider_account_id": "schwab_demo_001",
            "account_type": "brokerage", 
            "name": "Schwab Demo Account",
            "access_token": "mock_schwab_token_001"
        },
        {
            "provider": "plaid",
            "provider_account_id": "chase_demo_001",
            "account_type": "bank",
            "name": "Chase Checking",
            "access_token": "mock_plaid_token_001"
        }
    ]
    
    demo_accounts = []
    for account_data in accounts_data:
        account = Account(
            user_id=demo_user.id,
            **account_data,
            last_sync=datetime.utcnow() - timedelta(hours=random.randint(1, 24))
        )
        db.add(account)
        demo_accounts.append(account)
    
    db.commit()
    
    # Create demo holdings
    holdings_data = [
        {"symbol": "AAPL", "quantity": 10, "avg_cost": 150.00, "current_price": 175.50},
        {"symbol": "GOOGL", "quantity": 5, "avg_cost": 2800.00, "current_price": 2750.00},
        {"symbol": "TSLA", "quantity": 3, "avg_cost": 200.00, "current_price": 185.00},
        {"symbol": "MSFT", "quantity": 8, "avg_cost": 300.00, "current_price": 320.00},
        {"symbol": "NVDA", "quantity": 2, "avg_cost": 400.00, "current_price": 450.00},
    ]
    
    for i, holding_data in enumerate(holdings_data):
        holding = Holding(
            account_id=demo_accounts[i % len(demo_accounts)].id,
            **holding_data,
            value=holding_data["quantity"] * holding_data["current_price"]
        )
        db.add(holding)
    
    db.commit()
    
    # Create demo transactions
    transactions_data = [
        {
            "account_id": demo_accounts[0].id,
            "symbol": "AAPL",
            "type": "buy",
            "quantity": 10,
            "price": 150.00,
            "amount": 1500.00,
            "date": datetime.utcnow() - timedelta(days=30)
        },
        {
            "account_id": demo_accounts[0].id,
            "symbol": "GOOGL", 
            "type": "buy",
            "quantity": 5,
            "price": 2800.00,
            "amount": 14000.00,
            "date": datetime.utcnow() - timedelta(days=25)
        },
        {
            "account_id": demo_accounts[1].id,
            "symbol": "TSLA",
            "type": "buy", 
            "quantity": 3,
            "price": 200.00,
            "amount": 600.00,
            "date": datetime.utcnow() - timedelta(days=20)
        },
        {
            "account_id": demo_accounts[1].id,
            "symbol": "MSFT",
            "type": "buy",
            "quantity": 8,
            "price": 300.00,
            "amount": 2400.00,
            "date": datetime.utcnow() - timedelta(days=15)
        },
        {
            "account_id": demo_accounts[2].id,
            "symbol": "NVDA",
            "type": "buy",
            "quantity": 2,
            "price": 400.00,
            "amount": 800.00,
            "date": datetime.utcnow() - timedelta(days=10)
        }
    ]
    
    for transaction_data in transactions_data:
        transaction = Transaction(**transaction_data)
        db.add(transaction)
    
    db.commit()
    db.close()
