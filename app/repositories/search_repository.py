from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.repositories.base import SearchRepositoryInterface
from app.schemas.search import SearchResult
from app.models.company import Company
from app.data.fixtures import generate_mock_companies

class MockSearchRepository(SearchRepositoryInterface):

    def __init__(self):
        self._companies = generate_mock_companies(500)
    
    def search_companies(self, keyword: str) -> List[SearchResult]:
        if not keyword:
            return []

        keyword_lower = keyword.lower()

        results = [
            SearchResult(**company)
            for company in self._companies
            if self._matches_keyword(company, keyword_lower)
        ]

        return results[:100]
    
    def _matches_keyword(self, company: dict, keyword: str) -> bool:
        company_name = company["company_name"].lower()
        ticker = company["ticker"].lower()
        return keyword in company_name or keyword in ticker


class DBSearchRepository(SearchRepositoryInterface):
    
    def __init__(self, db: Session):
        self.db = db

    def search_companies(self, keyword: str) -> List[SearchResult]:
        if not keyword:
            return []

        companies = self.db.query(Company).filter(
            or_(
                Company.company_name.ilike(f"%{keyword}%"),
                Company.ticker.ilike(f"%{keyword}%")
            )
        ).limit(100).all()

        return [
            SearchResult.model_validate(company)
            for company in companies
        ]
