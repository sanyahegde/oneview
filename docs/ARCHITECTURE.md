# PortfolioAI Architecture

## System Overview

PortfolioAI is a full-stack personal portfolio management system consisting of three main components:

1. **iOS SwiftUI App** - Native mobile application
2. **FastAPI Backend** - REST API and data processing
3. **ML Module** - Sentiment analysis and price signal prediction

## Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   iOS SwiftUI   │    │  FastAPI Backend│    │   ML Module     │
│      App        │    │                 │    │                 │
│                 │    │                 │    │                 │
│ • SwiftUI Views │◄──►│ • REST API      │◄──►│ • scikit-learn  │
│ • Keychain      │    │ • SQLAlchemy    │    │ • Core ML       │
│ • Widgets       │    │ • Redis Cache   │    │ • Training     │
│ • Face ID       │    │ • Background    │    │ • Export       │
│                 │    │   Jobs          │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   External      │    │   PostgreSQL    │    │   Training      │
│   Aggregators   │    │   Database      │    │   Data          │
│                 │    │                 │    │                 │
│ • Robinhood     │    │ • Users         │    │ • Headlines     │
│ • Schwab        │    │ • Accounts      │    │ • Price Data    │
│ • Plaid         │    │ • Holdings      │    │ • Sentiment     │
│ • Akoya         │    │ • Transactions  │    │   Labels        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Component Details

### iOS SwiftUI App

**Technology Stack:**
- Swift 5.9+
- SwiftUI for UI
- Combine for reactive programming
- WidgetKit for home screen widgets
- LocalAuthentication for Face ID/Touch ID
- Keychain for secure token storage

**Key Features:**
- Tab-based navigation (Overview, Holdings, Accounts, Settings)
- Face ID/Touch ID authentication
- Real-time portfolio data
- Interactive charts and visualizations
- Home screen widgets
- Offline data caching

**Architecture Patterns:**
- MVVM (Model-View-ViewModel)
- Dependency Injection
- Repository pattern for data access
- Combine publishers for reactive data flow

### FastAPI Backend

**Technology Stack:**
- Python 3.11
- FastAPI for web framework
- SQLAlchemy 2.x for ORM
- Alembic for database migrations
- PostgreSQL for primary database
- Redis for caching
- Pydantic for data validation

**Key Features:**
- JWT-based authentication
- RESTful API design
- Mock aggregator integrations
- Background job processing
- Comprehensive test suite
- API documentation with Swagger

**Architecture Patterns:**
- Layered architecture (API → Service → Repository)
- Dependency injection
- Factory pattern for aggregators
- Observer pattern for background jobs

### ML Module

**Technology Stack:**
- Python 3.11
- scikit-learn for machine learning
- Core ML for iOS integration
- pandas for data manipulation
- yfinance for market data
- Jupyter notebooks for analysis

**Key Features:**
- Sentiment analysis on financial news
- Price signal prediction
- Core ML model export
- Training pipeline automation
- Model versioning and metrics

## Data Flow

### 1. User Authentication
```
iOS App → FastAPI → JWT Token → Keychain Storage
```

### 2. Account Linking
```
iOS App → FastAPI → Mock Aggregator → Database Storage
```

### 3. Data Synchronization
```
Background Job → Aggregator API → Data Processing → Database Update
```

### 4. Portfolio Display
```
iOS App → FastAPI API → Database Query → Formatted Response → UI Update
```

### 5. ML Inference
```
iOS App → Core ML Model → Sentiment Prediction → UI Display
```

## Security Architecture

### Authentication & Authorization
- JWT tokens with HS256 algorithm
- Token expiration and refresh
- Secure token storage in iOS Keychain
- CORS configuration for production

### Data Protection
- No credentials stored in repository
- Mock tokens for development
- Encrypted database connections
- Input validation and sanitization

### Privacy Considerations
- No personal financial data stored
- Mock aggregators for development
- Clear data usage policies
- User consent mechanisms

## Deployment Architecture

### Development Environment
```
┌─────────────────┐
│   Docker        │
│   Compose       │
│                 │
│ • FastAPI       │
│ • PostgreSQL    │
│ • Redis         │
│ • Alembic       │
└─────────────────┘
```

### Production Environment
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   Application   │    │   Database       │
│                 │    │   Servers       │    │   Cluster        │
│ • SSL/TLS       │◄──►│ • FastAPI       │    │ • PostgreSQL    │
│ • Rate Limiting │    │ • Gunicorn      │    │ • Redis Cache    │
│ • Health Checks │    │ • Auto-scaling  │    │ • Backups        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- Database connection pooling
- Redis clustering
- Load balancer distribution

### Performance Optimization
- Database indexing strategy
- Redis caching layer
- API response compression
- Background job queuing

### Monitoring & Observability
- Application metrics collection
- Error tracking and alerting
- Performance monitoring
- Health check endpoints

## Development Workflow

### Code Organization
```
portfolioai/
├── backend/           # FastAPI application
├── ios-app/          # SwiftUI application
├── ml-models/        # ML training and models
├── docs/             # Documentation
├── infra/            # Infrastructure as code
└── docker-compose.yml
```

### Testing Strategy
- Unit tests for business logic
- Integration tests for API endpoints
- UI tests for iOS app
- ML model validation tests

### CI/CD Pipeline
- Automated testing on pull requests
- Code quality checks (linting, type checking)
- Security vulnerability scanning
- Automated deployment to staging/production

## Future Enhancements

### Planned Features
- Real aggregator integrations (SnapTrade, Plaid)
- Advanced ML models (LSTM, Transformer)
- Real-time notifications
- Multi-user portfolio sharing
- Advanced analytics and reporting

### Technical Improvements
- GraphQL API implementation
- Microservices architecture
- Event-driven architecture
- Advanced caching strategies
- Machine learning pipeline automation
