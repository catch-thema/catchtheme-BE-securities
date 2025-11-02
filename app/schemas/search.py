from pydantic import BaseModel, Field
from typing import Optional

class SearchResult(BaseModel):
    company_name: str = Field(..., description="기업명")
    ticker: str = Field(..., description="종목 코드")

    class Config:
        from_attributes = True

class SearchResponse(BaseModel):
    status: int
    message: str
    data: Optional[list[SearchResult]] = None