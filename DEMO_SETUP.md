# PortfolioAI Demo Setup

## Quick Start Guide

### 1. Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Xcode 15+ (for iOS development)
- Git

### 2. Clone and Setup
```bash
git clone <repository-url>
cd portfolioai
make bootstrap
```

### 3. Start Backend Services
```bash
docker-compose up --build
```

### 4. Run Database Migrations
```bash
make migrate
```

### 5. Seed Demo Data
```bash
make seed
```

### 6. Start iOS App
```bash
open ios-app/PortfolioAI.xcodeproj
```

## Demo Credentials

### Default User Account
- **Email**: demo@portfolioai.com
- **Password**: demo123
- **Full Name**: Demo User

### Mock Account Tokens
- **Robinhood**: demo_robinhood_token_123
- **Schwab**: demo_schwab_token_456
- **Plaid**: demo_plaid_token_789
- **Akoya**: demo_akoya_token_101

## Demo Features

### Portfolio Dashboard
- Total portfolio value: $125,000
- Daily gain/loss: +$2,500 (+2.0%)
- Interactive performance chart
- Top holdings overview
- Market sentiment analysis

### Holdings
- **AAPL**: 10 shares @ $175.50
- **GOOGL**: 5 shares @ $2,750.00
- **TSLA**: 3 shares @ $185.00
- **MSFT**: 8 shares @ $320.00
- **NVDA**: 2 shares @ $450.00

### Account Types
- **Brokerage Accounts**: Robinhood, Schwab
- **Bank Accounts**: Chase (via Plaid), Wells Fargo (via Akoya)

### ML Features
- Sentiment analysis on financial headlines
- Price signal prediction models
- Core ML integration for iOS

## API Endpoints

### Base URL
- **Development**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Key Endpoints
- `POST /api/v1/auth/login` - User authentication
- `GET /api/v1/holdings/` - Portfolio holdings
- `GET /api/v1/transactions/` - Transaction history
- `POST /api/v1/accounts/link` - Link external accounts

## Development Commands

### Backend Development
```bash
# Start development server
make dev

# Run tests
make test

# Run linting
make lint

# Format code
make format

# Database operations
make migrate
make migrate-create MESSAGE="Add new feature"
```

### ML Development
```bash
# Train models
make ml-train

# Start Jupyter notebooks
make ml-notebooks
```

### iOS Development
```bash
# Build iOS app
make ios-build

# Run iOS tests
make ios-test

# Setup iOS dependencies
make setup-ios
```

## Troubleshooting

### Common Issues

#### Backend Won't Start
```bash
# Check Docker services
docker-compose ps

# View logs
docker-compose logs api

# Restart services
docker-compose restart
```

#### Database Connection Issues
```bash
# Check database status
docker-compose exec db pg_isready

# Connect to database
make db-shell
```

#### iOS Build Issues
```bash
# Clean build folder
cd ios-app
xcodebuild clean

# Reset package dependencies
swift package reset
```

### Performance Issues
- Ensure Docker has sufficient memory (4GB+)
- Close unnecessary applications
- Use SSD storage for better performance

## Production Deployment

### Environment Variables
Copy `env.example` to `.env` and update:
```bash
cp env.example .env
# Edit .env with production values
```

### Security Checklist
- [ ] Change default JWT secret
- [ ] Update database passwords
- [ ] Configure CORS origins
- [ ] Enable SSL/TLS
- [ ] Set up monitoring
- [ ] Configure backups

### Scaling Considerations
- Use production PostgreSQL cluster
- Implement Redis clustering
- Set up load balancing
- Configure auto-scaling
- Monitor performance metrics

## Support

### Documentation
- API Documentation: `/docs/API.md`
- Architecture: `/docs/ARCHITECTURE.md`
- Data Modeling: `/docs/DATA_MODELING.md`
- Privacy & Security: `/docs/PRIVACY_SECURITY.md`
- Roadmap: `/docs/ROADMAP.md`

### Getting Help
- Check the documentation first
- Review error logs
- Test with demo data
- Contact support if needed

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

**IMPORTANT**: This is a demo application for educational purposes only. The ML models and financial data are not intended for actual trading decisions. Use at your own risk.
