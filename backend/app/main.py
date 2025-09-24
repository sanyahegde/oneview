"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.v1 import auth, accounts, holdings, transactions
from app.db.init_db import init_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="PortfolioAI Backend API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(accounts.router, prefix=f"{settings.API_V1_STR}/accounts", tags=["accounts"])
app.include_router(holdings.router, prefix=f"{settings.API_V1_STR}/holdings", tags=["holdings"])
app.include_router(transactions.router, prefix=f"{settings.API_V1_STR}/transactions", tags=["transactions"])


@app.get("/health")
async def health_check() -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse({"status": "healthy", "service": "portfolioai-backend"})


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize database on startup."""
    await init_db()


@app.get("/")
async def root() -> JSONResponse:
    """Root endpoint."""
    return JSONResponse({
        "message": "PortfolioAI Backend API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    })
