from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings

app = FastAPI()

app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    return {
        "environment": settings.ENVIRONMENT,
        "use_mock_data": settings.USE_MOCK_DATA
    }