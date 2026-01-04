from fastapi import APIRouter
from app.api.v1.endpoints import portfolios, news, chatbot, plaid

api_router = APIRouter()
api_router.include_router(portfolios.router, prefix="/portfolios", tags=["portfolios"])
api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
api_router.include_router(plaid.router, prefix="/plaid", tags=["plaid"])

