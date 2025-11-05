from fastapi import APIRouter, Query, HTTPException
from app.schemas.stock_news import StockNewsResponse, NewsItem
from app.utils.naver_client import get_naver_search_client
from app.core.constants import HTTPStatus, Message, ErrorMessage, NaverAPIConfig
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/stock-news", response_model=StockNewsResponse)
def get_stock_news(
    stock_name: str = Query(..., description="종목명", min_length=1),
    display: int = Query(NaverAPIConfig.DEFAULT_DISPLAY, description="한 번에 가져올 뉴스 개수", ge=1, le=NaverAPIConfig.MAX_DISPLAY),
    sort: str = Query(NaverAPIConfig.SORT_DATE, description="정렬 방식 (sim: 정확도순, date: 최신순)")
):
    client = get_naver_search_client()

    result = client.search_news(
        query=stock_name,
        display=display,
        start=NaverAPIConfig.DEFAULT_START,
        sort=sort
    )

    if result is None:
        logger.error(f"Failed to fetch news for stock: {stock_name}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_ERROR,
            detail=ErrorMessage.NAVER_API_ERROR
        )

    items = result.get("items", [])

    if not items:
        return StockNewsResponse(
            status=HTTPStatus.OK,
            message=ErrorMessage.STOCK_NEWS_NOT_FOUND,
            data=[]
        )

    news_items = [
        NewsItem(
            title=item["title"],
            original_link=item["originallink"],
            link=item["link"],
            description=item["description"],
            pub_date=item["pubDate"]
        )
        for item in items
    ]

    return StockNewsResponse(
        status=HTTPStatus.OK,
        message=Message.GET_STOCK_NEWS_SUCCESS,
        data=news_items
    )
