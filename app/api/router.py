from fastapi import APIRouter
from app.api.endpoints import (
    health,
    search,
    stock_info,
    indices
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(search.router, prefix="/securities", tags=["search"])
api_router.include_router(stock_info.router, prefix="/securities", tags=["stock-info"])
api_router.include_router(indices.router, prefix="/securities", tags=["indices"])