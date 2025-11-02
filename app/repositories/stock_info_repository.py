from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.base import StockInfoRepositoryInterface
from app.schemas.stock_info import StockInfoDetail
from app.models.company import Company, StockInfo
from app.data.fixtures import get_mock_stock_info, MOCK_COMPANIES

class MockStockInfoRepository(StockInfoRepositoryInterface):

    def get_stock_info(self, ticker: str) -> Optional[StockInfoDetail]:
        company_exists = any(
            company["ticker"] == ticker
            for company in MOCK_COMPANIES
        ) or ticker.isdigit()

        if not company_exists:
            return None
        
        mock_data = get_mock_stock_info(ticker)

        return StockInfoDetail(**mock_data)

class DBStockInfoRepository(StockInfoRepositoryInterface):

    def __init__(self, db: Session):
        self.db = db
    
    def get_stock_info(self, ticker: str) -> Optional[StockInfoDetail]:
        stock_info = self.db.query(StockInfo).filter(
            StockInfo.ticker == ticker
        ).first()

        if not stock_info:
            return None
        
        return StockInfoDetail.model_validate(stock_info)
    