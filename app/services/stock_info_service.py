from typing import Optional
from app.schemas.stock_info import StockInfoDetail
from app.repositories.base import StockInfoRepositoryInterface

class StockInfoService:

    def __init__(self, repository: StockInfoRepositoryInterface):
        self.repository = repository
    
    def get_stock_info(self, ticker: str) -> Optional[StockInfoDetail]:        
        return self.repository.get_stock_info(ticker)