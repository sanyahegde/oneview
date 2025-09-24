# PortfolioAI Backend

FastAPI backend for PortfolioAI - a personal portfolio manager.

## Features

- JWT Authentication with Argon2 password hashing
- Account linking with mock aggregators (Robinhood, Schwab, Plaid, Akoya)
- Unified holdings and transactions API
- Portfolio snapshots and sentiment analysis
- PostgreSQL with SQLAlchemy 2.x and Alembic migrations
- Redis caching
- Comprehensive test suite

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start services:**
   ```bash
   docker-compose up db redis
   ```

3. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

4. **Start development server:**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **View API docs:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user

### Accounts
- `POST /api/v1/accounts/link` - Link external account
- `GET /api/v1/accounts` - List linked accounts

### Holdings
- `GET /api/v1/holdings` - Get unified holdings

### Transactions
- `GET /api/v1/transactions` - Get transactions with filters

### Snapshots
- `GET /api/v1/snapshots` - Get portfolio snapshots

### Sentiment
- `GET /api/v1/sentiment` - Get sentiment analysis

## Development

- **Tests**: `pytest tests/ -v`
- **Linting**: `ruff check app/ tests/`
- **Formatting**: `black app/ tests/`
- **Type checking**: `mypy app/`

## Environment Variables

See `.env.example` for required environment variables.
