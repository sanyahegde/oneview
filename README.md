# One View

A full-stack personal finance application that aggregates user investment holdings into a unified portfolio dashboard, allowing users to view net worth, asset allocation, and historical performance in a single interface.

## Features

- **Unified Portfolio Dashboard**: View all your investment holdings in one place
- **Net Worth Tracking**: Track total portfolio value and cost basis
- **Asset Allocation Visualization**: Interactive pie charts showing portfolio distribution
- **Sentiment Analysis**: AI-powered sentiment analysis on financial news for each stock
- **News Summarization**: LLM-based summarization of recent financial news per stock
- **Real-time Performance**: Gain/loss tracking with percentage calculations

## Tech Stack

- **Frontend**: React 18 + TypeScript + Vite
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **AI/ML**: OpenAI API (GPT-3.5-turbo) for sentiment analysis and news summarization
- **Data Visualization**: Recharts

## Project Structure

```
oneview/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Core configuration and database
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic (OpenAI, news, prices)
│   ├── alembic/         # Database migrations
│   └── requirements.txt
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   └── services/    # API client
│   └── package.json
└── docker-compose.yml   # PostgreSQL database setup
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or use Docker Compose)
- OpenAI API key

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/sanyahegde/one-view.git
cd one-view
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env and add your configuration:
# - DATABASE_URL: PostgreSQL connection string
# - OPENAI_API_KEY: Your OpenAI API key
# - SECRET_KEY: A random secret key for JWT (generate with: openssl rand -hex 32)
```

### 3. Database Setup

Using Docker Compose (recommended):

```bash
# From project root
docker-compose up -d
```

Or install PostgreSQL locally and update `DATABASE_URL` in `.env`.

### 4. Run Database Migrations

```bash
cd backend
alembic upgrade head
```

### 5. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file (optional, defaults work for local dev)
echo "VITE_API_BASE_URL=http://localhost:8000/api/v1" > .env
```

## Running the Application

### Start the Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation (Swagger UI): `http://localhost:8000/docs`

### Start the Frontend

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

1. **Create a Portfolio**: Use the API or add through the frontend
2. **Add Holdings**: Add stocks with symbol, quantity, and average cost
3. **View Dashboard**: See portfolio summary with net worth and asset allocation
4. **Monitor Sentiment**: View sentiment indicators for each stock based on recent news
5. **Read Summaries**: Get AI-generated summaries of relevant financial news

## API Endpoints

- `GET /api/v1/portfolios/` - List all portfolios
- `GET /api/v1/portfolios/{id}` - Get portfolio details
- `GET /api/v1/portfolios/{id}/summary` - Get portfolio summary with calculations
- `POST /api/v1/portfolios/{id}/holdings` - Add a holding
- `GET /api/v1/news/symbol/{symbol}` - Get news for a symbol
- `GET /api/v1/news/sentiment/{symbol}` - Get sentiment analysis for a symbol
- `GET /api/v1/news/portfolio/{id}/sentiments` - Get sentiments for all portfolio stocks

See full API documentation at `http://localhost:8000/docs`

## Development Notes

- The application uses mock data for stock prices and news in development mode
- Replace mock services with actual API integrations:
  - `app/services/price_service.py`: Integrate with stock price API (Alpha Vantage, Yahoo Finance, etc.)
  - `app/services/news_service.py`: Integrate with news API (Alpha Vantage News, NewsAPI, etc.)
- Authentication is currently simplified (hardcoded user ID). Implement proper JWT authentication for production.

## License

MIT
