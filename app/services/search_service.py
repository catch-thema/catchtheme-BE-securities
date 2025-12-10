from typing import List
from app.schemas.search import SearchResult
from app.repositories.base import SearchRepositoryInterface

class SearchService:

    def __init__(self, repository: SearchRepositoryInterface):
        self.repository = repository
    
    def search_companies(self, keyword: str) -> List[SearchResult]:
        return self.repository.search_companies(keyword)
