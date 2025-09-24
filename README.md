# PortfolioAI

A production-ready full-stack personal portfolio manager with iOS SwiftUI app, FastAPI backend, and ML module for sentiment analysis and basic predictions.

## Features

- **Unified Portfolio View**: Aggregate brokerage (Robinhood, Schwab) and bank balances in one interface
- **iOS App**: SwiftUI with Face ID, secure storage, charts, and widgets
- **FastAPI Backend**: Normalizes holdings/transactions from aggregators and exposes clean REST API
- **ML Layer**: Sentiment analysis and price signal predictions with Core ML export
- **Security**: JWT authentication, secure token storage, no credentials in repo

## Quick Start

1. **Bootstrap the project:**
   ```bash
   make bootstrap
   ```

2. **Start the backend services:**
   ```bash
   docker-compose up --build
   ```

3. **Run the iOS app:**
   ```bash
   open ios-app/PortfolioAI.xcodeproj
   ```

4. **Train ML models:**
   ```bash
   cd ml-models/src
   python train_sentiment.py
   python export_coreml.py
   ```

## Architecture

- **Backend**: Python 3.11, FastAPI, SQLAlchemy 2.x, PostgreSQL, Redis
- **iOS**: Swift 5.9+, SwiftUI, Combine, WidgetKit, Keychain
- **ML**: scikit-learn, Core ML, pandas, numpy, yfinance
- **Infrastructure**: Docker, GitHub Actions CI, pre-commit hooks

## Project Structure

```
portfolioai/
├── backend/           # FastAPI backend
├── ios-app/          # SwiftUI iOS application
├── ml-models/        # ML training and Core ML export
├── docs/             # Documentation
├── infra/            # CI/CD and configuration
└── docker-compose.yml
```

## Development

- **Backend API**: http://localhost:8000/docs (Swagger UI)
- **Database**: PostgreSQL on port 5432
- **Cache**: Redis on port 6379
- **Tests**: `make test` runs pytest suite
- **Linting**: `make lint` runs ruff, black, mypy

## Security & Privacy

- No credentials stored in repository
- JWT tokens stored securely in iOS Keychain
- Mock aggregators for development (replace with real providers)
- CORS configured for production iOS app scheme

## ML Models Disclaimer

**IMPORTANT**: All ML models in this project are for educational purposes only. They are not intended for actual trading advice or financial decisions. Use at your own risk.

## License

MIT License - see LICENSE file for details.
