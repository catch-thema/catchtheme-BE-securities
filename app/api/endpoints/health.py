from fastapi import APIRouter
from app.schemas.response import HealthResponse
from app.core.constants import HTTPStatus, Message

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status=HTTPStatus.OK,
        message=Message.HEALTH_CHECK_SUCCESS
    )
