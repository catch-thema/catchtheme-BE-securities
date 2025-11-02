from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class StockInfoDetail(BaseModel):

    current_price: Optional[int] = Field(None, description="현재가 (종가)")
    opening_price: Optional[int] = Field(None, description="시가")
    high_price: Optional[int] = Field(None, description="고가")
    low_price: Optional[int] = Field(None, description="저가")

    volume: Optional[int] = Field(None, description="거래량")
    transaction_amount: Optional[int] = Field(None, description="거래대금")

    market_cap: Optional[int] = Field(None, description="시가총액")
    per: Optional[Decimal] = Field(None, description="PER")
    pbr: Optional[Decimal] = Field(None, description="PBR")
    roe: Optional[Decimal] = Field(None, description="ROE")
    psr: Optional[Decimal] = Field(None, description="PSR")
    dividend_yield: Optional[Decimal] = Field(None, description="배당수익률")

    class Config:
        from_attributes = True

class StockInfoResponse(BaseModel):
    status: int
    message: str
    data: Optional[StockInfoDetail] = None
