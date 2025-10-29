from pydantic import BaseModel, Field
from typing import Optional

class CompanyInfo(BaseModel):
    company_name: str = Field(..., description="기업명")
    ticker: str = Field(..., description="종목 코드")

class CompanySearchResponse(BaseModel):
    status: str
    message: str
    data: Optional[list[CompanyInfo]] = None