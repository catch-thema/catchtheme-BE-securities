from fastapi import APIRouter
from app.api.endpoints import (
    health,
    search,
    stock_info,
    exchange_rate,
    stock_news
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(search.router, prefix="/securities", tags=["search"])
api_router.include_router(stock_info.router, prefix="/securities", tags=["stock-info"])
api_router.include_router(exchange_rate.router, prefix="/securities", tags=["exchange-rate"])
api_router.include_router(stock_news.router, prefix="/securities", tags=["stock-news"])