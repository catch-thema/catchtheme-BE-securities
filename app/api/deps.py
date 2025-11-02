from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import get_db
from app.core.config import settings
from app.repositories.search_repository import MockSearchRepository, DBSearchRepository
from app.repositories.stock_info_repository import MockStockInfoRepository, DBStockInfoRepository

def get_search_repository(db: Session = Depends(get_db)):
    if settings.USE_MOCK_DATA:
        return MockSearchRepository()
    return DBSearchRepository(db)

def get_stock_info_repository(db: Session = Depends(get_db)):
    if settings.USE_MOCK_DATA:
        return MockStockInfoRepository()
    return DBStockInfoRepository(db)