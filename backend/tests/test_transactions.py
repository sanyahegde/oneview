"""Transaction tests."""

import pytest
from fastapi.testclient import TestClient


def test_get_transactions(client: TestClient, auth_headers, test_transaction):
    """Test getting user transactions."""
    response = client.get("/api/v1/transactions/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "pages" in data
    
    assert isinstance(data["items"], list)
    assert len(data["items"]) >= 1


def test_get_transactions_empty(client: TestClient, auth_headers):
    """Test getting transactions for user with no accounts."""
    # Create a new user without accounts
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "notransactions@example.com",
            "password": "password123",
            "full_name": "No Transactions User"
        }
    )
    
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "notransactions@example.com",
            "password": "password123"
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/v1/transactions/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


def test_get_transactions_unauthorized(client: TestClient):
    """Test getting transactions without authentication."""
    response = client.get("/api/v1/transactions/")
    assert response.status_code == 403


def test_transaction_filters_symbol(client: TestClient, auth_headers, test_transaction):
    """Test filtering transactions by symbol."""
    response = client.get(
        "/api/v1/transactions/?symbol=AAPL",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    
    # All transactions should be AAPL
    for transaction in data["items"]:
        assert transaction["symbol"] == "AAPL"


def test_transaction_filters_type(client: TestClient, auth_headers, test_transaction):
    """Test filtering transactions by type."""
    response = client.get(
        "/api/v1/transactions/?type=buy",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    
    # All transactions should be buy type
    for transaction in data["items"]:
        assert transaction["type"] == "buy"


def test_transaction_pagination(client: TestClient, auth_headers, test_account, db_session):
    """Test transaction pagination."""
    # Add multiple transactions
    from app.models.transaction import Transaction, TransactionType
    from datetime import datetime
    
    transactions = []
    for i in range(15):
        transaction = Transaction(
            account_id=test_account.id,
            symbol="AAPL",
            type=TransactionType.BUY,
            quantity=1.0,
            price=150.0 + i,
            amount=150.0 + i,
            date=datetime(2024, 1, i + 1),
            description=f"Transaction {i + 1}"
        )
        transactions.append(transaction)
    
    db_session.add_all(transactions)
    db_session.commit()
    
    # Test first page
    response = client.get(
        "/api/v1/transactions/?page=1&page_size=10",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert data["total"] >= 15
    
    # Test second page
    response = client.get(
        "/api/v1/transactions/?page=2&page_size=10",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 5  # At least 5 more transactions
    assert data["page"] == 2


def test_transaction_data_structure(client: TestClient, auth_headers, test_transaction):
    """Test transaction data structure."""
    response = client.get("/api/v1/transactions/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    
    transaction = data["items"][0]
    assert "id" in transaction
    assert "account_id" in transaction
    assert "symbol" in transaction
    assert "type" in transaction
    assert "quantity" in transaction
    assert "price" in transaction
    assert "amount" in transaction
    assert "date" in transaction
    assert "description" in transaction


def test_transaction_filters_combined(client: TestClient, auth_headers, test_account, db_session):
    """Test combined transaction filters."""
    from app.models.transaction import Transaction, TransactionType
    from datetime import datetime
    
    # Add transactions with different types and symbols
    transactions = [
        Transaction(
            account_id=test_account.id,
            symbol="AAPL",
            type=TransactionType.BUY,
            quantity=10.0,
            price=150.0,
            amount=1500.0,
            date=datetime(2024, 1, 15),
            description="Buy AAPL"
        ),
        Transaction(
            account_id=test_account.id,
            symbol="GOOGL",
            type=TransactionType.SELL,
            quantity=5.0,
            price=2800.0,
            amount=14000.0,
            date=datetime(2024, 1, 20),
            description="Sell GOOGL"
        )
    ]
    
    db_session.add_all(transactions)
    db_session.commit()
    
    # Filter by symbol and type
    response = client.get(
        "/api/v1/transactions/?symbol=AAPL&type=buy",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    
    # Should only return AAPL buy transactions
    for transaction in data["items"]:
        assert transaction["symbol"] == "AAPL"
        assert transaction["type"] == "buy"
