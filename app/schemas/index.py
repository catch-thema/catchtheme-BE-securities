from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class IndexData(BaseModel):
    code: str = Field(..., description="지수 코드 (KOSPI, KOSDAQ, NASDAQ, SP500)")
    name: str = Field(..., description="지수 명")
    current_price: Decimal = Field(..., description="현재가")
    change_rate: Decimal = Field(..., description="등락률 (%)")
    change_price: Decimal = Field(..., description="전일대비")
    timestamp: str = Field(..., description="데이터 시간")


class IndexListResponse(BaseModel):
    indices: list[IndexData] = Field(..., description="지수 목록")
