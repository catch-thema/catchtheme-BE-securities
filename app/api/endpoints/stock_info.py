from fastapi import APIRouter, Path, Depends, HTTPException
from app.schemas.stock_info import StockInfoResponse
from app.services.stock_info_service import StockInfoService
from app.core.constants import HTTPStatus, Message, ErrorMessage
from app.api.deps import get_stock_info_repository
from app.repositories.base import StockInfoRepositoryInterface

router = APIRouter()

@router.get("/companies/stocks/{ticker}", response_model=StockInfoResponse)
def get_stock_info(
    ticker: str = Path(..., description="종목 코드 (예: 005930)", min_length=6, max_length=6),
    repository: StockInfoRepositoryInterface = Depends(get_stock_info_repository)
):
    service = StockInfoService(repository)
    stock_info = service.get_stock_info(ticker)

    if not stock_info:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail={
                "status": HTTPStatus.NOT_FOUND,
                "message": ErrorMessage.STOCK_NOT_FOUND,
                "data": None
            }
        )
    
    return StockInfoResponse(
        status=HTTPStatus.OK,
        message=Message.GET_STOCK_INFO_SUCCESS,
        data=stock_info
    )