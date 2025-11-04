from fastapi import APIRouter, Path, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.stock_detail import StockDetailResponse
from app.repositories.stock_detail_repository import KISStockDetailRepository
from app.core.constants import HTTPStatus, ErrorMessage, Message
from app.db.session import get_db

router = APIRouter()


@router.get("/stocks/{ticker}", response_model=StockDetailResponse)
def get_stock_info(
    ticker: str = Path(..., description="종목 코드 (예: 005930)", min_length=6, max_length=6),
    db: Session = Depends(get_db)
):
    repository = KISStockDetailRepository()
    stock_detail = repository.get_stock_detail(ticker, db=db)

    if not stock_detail:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail={
                "status": HTTPStatus.NOT_FOUND,
                "message": ErrorMessage.STOCK_NOT_FOUND,
                "data": None
            }
        )

    return StockDetailResponse(
        status=HTTPStatus.OK,
        message=Message.GET_STOCK_INFO_SUCCESS,
        data=stock_detail
    )