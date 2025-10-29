from fastapi import APIRouter, Query, Depends
from app.schemas.search import SearchResponse
from app.services.search_service import SearchService
from app.core.constants import Status, Message
from app.api.deps import get_search_repository
from app.repositories.base import SearchRepositoryInterface

router = APIRouter()

@router.get("/search", response_model=SearchResponse)
def search_company(
    keyword: str = Query(..., description="검색 키워드 (기업명 또는 종목 코드)", min_length=1),
    repository: SearchRepositoryInterface = Depends(get_search_repository)
):
    search_service = SearchService(repository)
    results = search_service.search_companies(keyword)

    if not results:
        return SearchResponse(
            status=Status.OK,
            message=Message.COMPANY_SEARCH_NOT_FOUND,
            data=[]
        )
    
    return SearchResponse(
        status=Status.OK,
        message=Message.COMPANY_SEARCH_SUCCESS,
        data=results
    )