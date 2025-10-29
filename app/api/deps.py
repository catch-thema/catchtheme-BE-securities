from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import get_db
from app.core.config import settings
from app.repositories.base import SearchRepositoryInterface
from app.repositories.search_repository import (
    MockSearchRepository,
    DBSearchRepository
)

def get_search_repository(
    db: Session = Depends(get_db)
) -> SearchRepositoryInterface:
    if settings.USE_MOCK_DATA:
        return MockSearchRepository()
    return DBSearchRepository(db)