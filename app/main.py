from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings
from app.scheduler.exchange_rate_scheduler import start_scheduler, shutdown_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    shutdown_scheduler()

app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {
        "environment": settings.ENVIRONMENT,
        "use_mock_data": settings.USE_MOCK_DATA
    }