from pydantic import BaseModel, Field
from typing import Optional, List


class StockInfo(BaseModel):
    standard_code: str = Field(..., description="표준코드 (12자리)")
    short_code: str = Field(..., description="단축코드 (6자리)")
    korean_name: str = Field(..., description="한글 종목명")
    korean_short_name: Optional[str] = Field(None, description="한글 종목약명")
    english_name: Optional[str] = Field(None, description="영문 종목명")
    listing_date: Optional[str] = Field(None, description="상장일 (YYYY/MM/DD)")
    market_type: Optional[str] = Field(None, description="시장구분 (KOSPI, KOSDAQ, etc)")
    security_type: Optional[str] = Field(None, description="증권구분")
    sector: Optional[str] = Field(None, description="소속부")
    stock_type: Optional[str] = Field(None, description="주식종류")
    par_value: Optional[int] = Field(None, description="액면가")
    listed_shares: Optional[int] = Field(None, description="상장주식수")


class PaginationMeta(BaseModel):
    total: int = Field(..., description="전체 종목 수")
    page: int = Field(..., description="현재 페이지")
    count: int = Field(..., description="페이지당 항목 수")
    total_pages: int = Field(..., description="전체 페이지 수")


class StockListData(BaseModel):
    items: List[StockInfo] = Field(..., description="종목 목록")
    pagination: PaginationMeta = Field(..., description="페이지네이션 정보")


class StockListResponse(BaseModel):
    status: int
    message: str
    data: Optional[StockListData] = None
