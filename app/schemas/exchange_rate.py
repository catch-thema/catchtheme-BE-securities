from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field

class ExchangeRateData(BaseModel):
    base_rate: Decimal = Field(..., description="기준율 (매매기준율)")
    change_rate: Optional[Decimal] = Field(None, description="등락률 (%)")

    class Config:
        from_attributes = True

class ExchangeRateResponse(BaseModel):
    status: int
    message: str
    data: Optional[ExchangeRateData] = None
