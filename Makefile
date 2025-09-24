.PHONY: bootstrap dev test lint format migrate seed clean help

# Default target
help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

bootstrap: ## Install dependencies and setup development environment
	@echo "🚀 Bootstrapping PortfolioAI..."
	pip install pre-commit
	pre-commit install
	cd backend && pip install -r requirements.txt
	cd ml-models/src && pip install -r requirements.txt
	@echo "✅ Bootstrap complete!"

dev: ## Start development environment
	@echo "🔧 Starting development environment..."
	docker-compose up --build

test: ## Run tests
	@echo "🧪 Running tests..."
	cd backend && python -m pytest tests/ -v --cov=app --cov-report=html

test-watch: ## Run tests in watch mode
	@echo "👀 Running tests in watch mode..."
	cd backend && python -m pytest tests/ -v --cov=app -f

lint: ## Run linting
	@echo "🔍 Running linters..."
	cd backend && ruff check app/ tests/
	cd backend && black --check app/ tests/
	cd backend && mypy app/

format: ## Format code
	@echo "✨ Formatting code..."
	cd backend && ruff check --fix app/ tests/
	cd backend && black app/ tests/

migrate: ## Run database migrations
	@echo "🗄️ Running database migrations..."
	cd backend && alembic upgrade head

migrate-create: ## Create new migration
	@echo "📝 Creating new migration..."
	cd backend && alembic revision --autogenerate -m "$(MESSAGE)"

seed: ## Seed database with demo data
	@echo "🌱 Seeding database..."
	cd backend && python -c "from app.db.init_db import init_db; init_db()"

clean: ## Clean up containers and volumes
	@echo "🧹 Cleaning up..."
	docker-compose down -v
	docker system prune -f

logs: ## Show logs
	@echo "📋 Showing logs..."
	docker-compose logs -f

shell: ## Open shell in API container
	@echo "🐚 Opening shell..."
	docker-compose exec api /bin/bash

db-shell: ## Open database shell
	@echo "🗄️ Opening database shell..."
	docker-compose exec db psql -U portfolioai -d portfolioai

ml-train: ## Train ML models
	@echo "🤖 Training ML models..."
	cd ml-models/src && python train_sentiment.py
	cd ml-models/src && python train_price_signal.py
	cd ml-models/src && python export_coreml.py

ml-notebooks: ## Start Jupyter notebooks for ML
	@echo "📓 Starting Jupyter notebooks..."
	cd ml-models && jupyter notebook

ios-build: ## Build iOS app (requires Xcode)
	@echo "📱 Building iOS app..."
	cd ios-app && xcodebuild -project PortfolioAI.xcodeproj -scheme PortfolioAI -destination 'platform=iOS Simulator,name=iPhone 15' build

ios-test: ## Run iOS tests (requires Xcode)
	@echo "🧪 Running iOS tests..."
	cd ios-app && xcodebuild -project PortfolioAI.xcodeproj -scheme PortfolioAI -destination 'platform=iOS Simulator,name=iPhone 15' test

setup-ios: ## Setup iOS development environment
	@echo "📱 Setting up iOS development..."
	cd ios-app && swift package resolve

# Development shortcuts
up: dev ## Alias for dev
down: ## Stop all services
	docker-compose down

restart: ## Restart all services
	docker-compose restart

status: ## Show service status
	docker-compose ps
