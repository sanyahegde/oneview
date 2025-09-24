# PortfolioAI API Documentation

## Overview

PortfolioAI provides a RESTful API for managing personal portfolios, including account linking, holdings tracking, transaction history, and sentiment analysis.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.portfolioai.com`

## Authentication

All API endpoints (except registration and login) require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## API Endpoints

### Authentication

#### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Login User
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /api/v1/auth/me
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Accounts

#### Link Account
```http
POST /api/v1/accounts/link
Authorization: Bearer <token>
Content-Type: application/json

{
  "provider": "robinhood",
  "public_token": "public_token_123"
}
```

**Response:**
```json
{
  "account_id": 1,
  "provider": "robinhood",
  "status": "linked"
}
```

#### Get Accounts
```http
GET /api/v1/accounts/
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "provider": "robinhood",
    "provider_account_id": "rh_123",
    "account_type": "brokerage",
    "name": "Robinhood Account",
    "last_sync": "2024-01-01T12:00:00Z",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### Holdings

#### Get Holdings
```http
GET /api/v1/holdings/
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "symbol": "AAPL",
    "quantity": 10.0,
    "avg_cost": 150.0,
    "current_price": 175.0,
    "value": 1750.0,
    "account_id": 1,
    "account_name": "Robinhood Account",
    "provider": "robinhood"
  }
]
```

### Transactions

#### Get Transactions
```http
GET /api/v1/transactions/?symbol=AAPL&type=buy&page=1&page_size=50
Authorization: Bearer <token>
```

**Query Parameters:**
- `symbol` (optional): Filter by symbol
- `type` (optional): Filter by transaction type (buy, sell, dividend, deposit, withdrawal)
- `date_from` (optional): Start date (ISO 8601)
- `date_to` (optional): End date (ISO 8601)
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 50, max: 100)

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "account_id": 1,
      "symbol": "AAPL",
      "type": "buy",
      "quantity": 10.0,
      "price": 150.0,
      "amount": 1500.0,
      "date": "2024-01-01T00:00:00Z",
      "description": "Buy AAPL shares",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 50,
  "pages": 1
}
```

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message description"
}
```

### Common HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

## Example Usage

### cURL Examples

#### Register and Login
```bash
# Register
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@example.com", "password": "demo123", "full_name": "Demo User"}'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@example.com", "password": "demo123"}'
```

#### Get Holdings
```bash
curl -X GET "http://localhost:8000/api/v1/holdings/" \
  -H "Authorization: Bearer <your_token>"
```

#### Link Account
```bash
curl -X POST "http://localhost:8000/api/v1/accounts/link" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"provider": "robinhood", "public_token": "demo_token"}'
```

## Rate Limiting

- **Authentication endpoints**: 10 requests per minute
- **Data endpoints**: 100 requests per minute
- **Bulk operations**: 5 requests per minute

## SDKs

- **iOS**: Swift package included in the project
- **Python**: Use `httpx` or `requests` library
- **JavaScript**: Use `fetch` or `axios`

## Support

For API support, please contact: api-support@portfolioai.com
