from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings
from app.services.index_manager import get_index_manager
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting IndexDataManager...")
    manager = await get_index_manager()
    logger.info("IndexDataManager started successfully")

    yield

    logger.info("Shutting down IndexDataManager...")
    await manager.stop()
    logger.info("IndexDataManager stopped")


app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api")


@app.get("/")
def root():
    return {
        "environment": settings.ENVIRONMENT,
        "use_mock_data": settings.USE_MOCK_DATA
    }