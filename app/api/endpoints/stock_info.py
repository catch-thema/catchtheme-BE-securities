from fastapi import APIRouter, Path, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from app.schemas.stock_detail import StockDetailResponse
from app.schemas.stock_chart import StockChartResponse
from app.repositories.stock_detail_repository import KISStockDetailRepository
from app.repositories.stock_chart_repository import KISStockChartRepository
from app.core.constants import HTTPStatus, ErrorMessage, Message, KISAPIConfig
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


@router.get("/stocks/{ticker}/chart", response_model=StockChartResponse)
def get_stock_chart(
    ticker: str = Path(..., description="종목 코드 (예: 005930)", min_length=6, max_length=6),
    start_date: str = Query(..., description="조회 시작일자 (YYYYMMDD)", regex="^[0-9]{8}$"),
    end_date: str = Query(..., description="조회 종료일자 (YYYYMMDD)", regex="^[0-9]{8}$"),
    period: str = Query(
        default=KISAPIConfig.PERIOD_DIV_CODE_DAY,
        description="기간 구분 코드 (D:일봉, W:주봉, M:월봉, Y:년봉)",
        regex="^[DWMY]$"
    ),
    adjusted: str = Query(
        default=KISAPIConfig.ADJUSTED_PRICE_TYPE_ADJUSTED,
        description="수정주가 여부 (0:수정주가, 1:원주가)",
        regex="^[01]$"
    )
):
    valid_periods = {
        KISAPIConfig.PERIOD_DIV_CODE_DAY,
        KISAPIConfig.PERIOD_DIV_CODE_WEEK,
        KISAPIConfig.PERIOD_DIV_CODE_MONTH,
        KISAPIConfig.PERIOD_DIV_CODE_YEAR
    }

    if period not in valid_periods:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={
                "status": HTTPStatus.BAD_REQUEST,
                "message": ErrorMessage.INVALID_PERIOD_TYPE,
                "data": None
            }
        )

    if start_date > end_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={
                "status": HTTPStatus.BAD_REQUEST,
                "message": ErrorMessage.INVALID_DATE_RANGE,
                "data": None
            }
        )

    repository = KISStockChartRepository()
    stock_chart = repository.get_stock_chart(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        period_div_code=period,
        adjusted_price_type=adjusted
    )

    if not stock_chart:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail={
                "status": HTTPStatus.NOT_FOUND,
                "message": ErrorMessage.STOCK_CHART_NOT_FOUND,
                "data": None
            }
        )

    return StockChartResponse(
        status=HTTPStatus.OK,
        message=Message.GET_STOCK_CHART_SUCCESS,
        data=stock_chart
    )