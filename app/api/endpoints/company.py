from fastapi import APIRouter, Query
from app.schemas.company import CompanySearchResponse
from app.services.company_service import company_service
from app.core.constants import Status, Message

router = APIRouter()

@router.get("/search", response_model=CompanySearchResponse)
def search_company(
    keyword: str = Query(..., description="검색 키워드 (기업명 또는 종목 코드)")
):
    companies = company_service.search_companies(keyword)

    if not companies:
        return CompanySearchResponse(
            status=Status.OK,
            message=Message.COMPANY_NOT_FOUND,
            data=[]
        )
    
    return CompanySearchResponse(
        status=Status.OK,
        message=Message.COMPANY_SEARCH_SUCCESS,
        data=companies
    )