"""Configuration settings for the application."""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    DATABASE_URL: str = "postgresql://portfolioai:password@localhost:5432/portfolioai"
    TEST_DATABASE_URL: str = "postgresql://portfolioai:password@localhost:5432/portfolioai_test"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    JWT_SECRET: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "portfolioai://app"
    ]
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "PortfolioAI"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    
    # External Services (Mock URLs)
    ROBINHOOD_API_URL: str = "https://api.robinhood.com"
    SCHWAB_API_URL: str = "https://api.schwab.com"
    PLAID_API_URL: str = "https://api.plaid.com"
    AKOYA_API_URL: str = "https://api.akoya.com"
    
    # ML Configuration
    ML_MODELS_PATH: str = "./ml-models/models"
    SENTIMENT_MODEL_PATH: str = "./ml-models/models/sentiment.mlmodel"
    PRICE_SIGNAL_MODEL_PATH: str = "./ml-models/models/price_signal.mlmodel"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = True


settings = Settings()
