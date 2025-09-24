"""Test configuration and fixtures."""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User
from app.models.account import Account, AccountType
from app.models.holding import Holding
from app.models.transaction import Transaction, TransactionType


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def db_session():
    """Create a test database session."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """Create a test client."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_account(db_session, test_user):
    """Create a test account."""
    account = Account(
        user_id=test_user.id,
        provider="robinhood",
        provider_account_id="test_account_001",
        account_type=AccountType.BROKERAGE,
        name="Test Brokerage Account",
        access_token="test_access_token"
    )
    db_session.add(account)
    db_session.commit()
    db_session.refresh(account)
    return account


@pytest.fixture
def test_holding(db_session, test_account):
    """Create a test holding."""
    holding = Holding(
        account_id=test_account.id,
        symbol="AAPL",
        quantity=10.0,
        avg_cost=150.0,
        current_price=175.0,
        value=1750.0
    )
    db_session.add(holding)
    db_session.commit()
    db_session.refresh(holding)
    return holding


@pytest.fixture
def test_transaction(db_session, test_account):
    """Create a test transaction."""
    transaction = Transaction(
        account_id=test_account.id,
        symbol="AAPL",
        type=TransactionType.BUY,
        quantity=10.0,
        price=150.0,
        amount=1500.0,
        date="2024-01-01T00:00:00Z",
        description="Buy AAPL shares"
    )
    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)
    return transaction


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers for test user."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": test_user.email, "password": "testpassword"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
