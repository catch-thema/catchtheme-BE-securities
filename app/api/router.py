from fastapi import APIRouter
from app.api.endpoints import health, company

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(company.router, prefix="/securities", tags=["securities"])