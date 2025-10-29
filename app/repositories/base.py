from abc import ABC, abstractmethod
from typing import List
from app.schemas.search import SearchResult

class SearchRepositoryInterface(ABC):

    @abstractmethod
    def search_companies(self, keyword: str) -> List[SearchResult]:
        pass