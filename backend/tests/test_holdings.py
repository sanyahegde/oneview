"""Holdings tests."""

import pytest
from fastapi.testclient import TestClient


def test_get_holdings(client: TestClient, auth_headers, test_holding):
    """Test getting user holdings."""
    response = client.get("/api/v1/holdings/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    # Check holding structure
    holding = data[0]
    assert "symbol" in holding
    assert "quantity" in holding
    assert "avg_cost" in holding
    assert "current_price" in holding
    assert "value" in holding
    assert "account_id" in holding


def test_get_holdings_empty(client: TestClient, auth_headers):
    """Test getting holdings for user with no accounts."""
    # Create a new user without accounts
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "noholdings@example.com",
            "password": "password123",
            "full_name": "No Holdings User"
        }
    )
    
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "noholdings@example.com",
            "password": "password123"
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/v1/holdings/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data == []


def test_get_holdings_unauthorized(client: TestClient):
    """Test getting holdings without authentication."""
    response = client.get("/api/v1/holdings/")
    assert response.status_code == 403


def test_holdings_data_structure(client: TestClient, auth_headers, test_holding):
    """Test holdings data structure."""
    response = client.get("/api/v1/holdings/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    
    holding = data[0]
    assert holding["symbol"] == "AAPL"
    assert holding["quantity"] == 10.0
    assert holding["avg_cost"] == 150.0
    assert holding["current_price"] == 175.0
    assert holding["value"] == 1750.0


def test_multiple_holdings(client: TestClient, auth_headers, test_account, db_session):
    """Test getting multiple holdings."""
    # Add another holding
    from app.models.holding import Holding
    holding2 = Holding(
        account_id=test_account.id,
        symbol="GOOGL",
        quantity=5.0,
        avg_cost=2800.0,
        current_price=2750.0,
        value=13750.0
    )
    db_session.add(holding2)
    db_session.commit()
    
    response = client.get("/api/v1/holdings/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    symbols = [h["symbol"] for h in data]
    assert "AAPL" in symbols
    assert "GOOGL" in symbols


def test_holdings_with_multiple_accounts(client: TestClient, auth_headers, test_user, db_session):
    """Test holdings across multiple accounts."""
    # Create another account
    from app.models.account import Account, AccountType
    account2 = Account(
        user_id=test_user.id,
        provider="schwab",
        provider_account_id="test_account_002",
        account_type=AccountType.BROKERAGE,
        name="Test Schwab Account",
        access_token="test_access_token_2"
    )
    db_session.add(account2)
    db_session.commit()
    db_session.refresh(account2)
    
    # Add holding to second account
    from app.models.holding import Holding
    holding2 = Holding(
        account_id=account2.id,
        symbol="MSFT",
        quantity=8.0,
        avg_cost=300.0,
        current_price=320.0,
        value=2560.0
    )
    db_session.add(holding2)
    db_session.commit()
    
    response = client.get("/api/v1/holdings/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    
    # Check that holdings from both accounts are included
    symbols = [h["symbol"] for h in data]
    assert "AAPL" in symbols
    assert "MSFT" in symbols
