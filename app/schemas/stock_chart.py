from typing import Optional, List
from pydantic import BaseModel, Field


class StockChartSummary(BaseModel):
    previous_day_diff: Optional[int] = Field(None, description="전일 대비")
    previous_day_diff_sign: Optional[str] = Field(None, description="전일 대비 부호")
    previous_day_change_rate: Optional[str] = Field(None, description="전일 대비율")
    previous_day_close: Optional[int] = Field(None, description="주식 전일 종가")
    accumulated_volume: Optional[int] = Field(None, description="누적 거래량")
    accumulated_transaction_amount: Optional[int] = Field(None, description="누적 거래 대금")
    stock_name: Optional[str] = Field(None, description="종목명")
    current_price: Optional[int] = Field(None, description="주식 현재가")


class StockChartDataPoint(BaseModel):
    date: str = Field(..., description="영업일자 (YYYYMMDD)")
    close_price: int = Field(..., description="종가")
    open_price: int = Field(..., description="시가")
    high_price: int = Field(..., description="고가")
    low_price: int = Field(..., description="저가")
    volume: int = Field(..., description="거래량")
    transaction_amount: int = Field(..., description="거래대금")


class StockChartInfo(BaseModel):
    summary: StockChartSummary = Field(..., description="차트 요약 정보")
    chart_data: List[StockChartDataPoint] = Field(..., description="시세 데이터")


class StockChartResponse(BaseModel):
    status: int = Field(..., description="응답 상태 코드")
    message: str = Field(..., description="응답 메시지")
    data: Optional[StockChartInfo] = Field(None, description="차트 데이터")
