from abc import ABC, abstractmethod
from typing import List, Optional
from app.schemas.search import SearchResult
from app.schemas.stock_info import StockInfoDetail

class SearchRepositoryInterface(ABC):

    @abstractmethod
    def search_companies(self, keyword: str) -> List[SearchResult]:
        pass

class StockInfoRepositoryInterface(ABC):

    @abstractmethod
    def get_stock_info(self, ticker: str) -> Optional[StockInfoDetail]:
        pass