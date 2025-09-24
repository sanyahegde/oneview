"""Account tests."""

import pytest
from fastapi.testclient import TestClient


def test_link_brokerage_account(client: TestClient, auth_headers):
    """Test linking a brokerage account."""
    response = client.post(
        "/api/v1/accounts/link",
        json={
            "provider": "robinhood",
            "public_token": "test_public_token_123"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "robinhood"
    assert data["status"] == "linked"
    assert "account_id" in data


def test_link_bank_account(client: TestClient, auth_headers):
    """Test linking a bank account."""
    response = client.post(
        "/api/v1/accounts/link",
        json={
            "provider": "plaid",
            "public_token": "test_public_token_456"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "plaid"
    assert data["status"] == "linked"


def test_link_unsupported_provider(client: TestClient, auth_headers):
    """Test linking an unsupported provider."""
    response = client.post(
        "/api/v1/accounts/link",
        json={
            "provider": "unsupported",
            "public_token": "test_token"
        },
        headers=auth_headers
    )
    assert response.status_code == 400
    assert "Unsupported provider" in response.json()["detail"]


def test_link_account_unauthorized(client: TestClient):
    """Test linking account without authentication."""
    response = client.post(
        "/api/v1/accounts/link",
        json={
            "provider": "robinhood",
            "public_token": "test_token"
        }
    )
    assert response.status_code == 403


def test_get_accounts(client: TestClient, auth_headers, test_account):
    """Test getting user accounts."""
    response = client.get("/api/v1/accounts/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["id"] == test_account.id


def test_get_accounts_empty(client: TestClient, auth_headers):
    """Test getting accounts for user with no accounts."""
    # Create a new user without accounts
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "noaccounts@example.com",
            "password": "password123",
            "full_name": "No Accounts User"
        }
    )
    
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "noaccounts@example.com",
            "password": "password123"
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/v1/accounts/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data == []


def test_get_specific_account(client: TestClient, auth_headers, test_account):
    """Test getting a specific account."""
    response = client.get(f"/api/v1/accounts/{test_account.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_account.id
    assert data["provider"] == test_account.provider


def test_get_nonexistent_account(client: TestClient, auth_headers):
    """Test getting a nonexistent account."""
    response = client.get("/api/v1/accounts/99999", headers=auth_headers)
    assert response.status_code == 404
    assert "Account not found" in response.json()["detail"]


def test_get_account_unauthorized(client: TestClient, test_account):
    """Test getting account without authentication."""
    response = client.get(f"/api/v1/accounts/{test_account.id}")
    assert response.status_code == 403
