from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.constants import HTTPStatus, Message, ErrorMessage
from app.schemas.exchange_rate import ExchangeRateResponse
from app.repositories.exchange_rate_repository import ExchangeRateRepository

router = APIRouter()

@router.get("/exchange-rates/usd", response_model=ExchangeRateResponse)
def get_usd_exchange_rate(db: Session = Depends(get_db)):
    repository = ExchangeRateRepository()
    exchange_rate = repository.get_usd_exchange_rate(db=db)

    if not exchange_rate:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail={
                "status": HTTPStatus.NOT_FOUND,
                "message": ErrorMessage.EXCHANGE_RATE_NOT_FOUND,
                "data": None
            }
        )

    return ExchangeRateResponse(
        status=HTTPStatus.OK,
        message=Message.GET_EXCHANGE_RATE_SUCCESS,
        data=exchange_rate
    )
