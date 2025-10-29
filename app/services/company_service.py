from typing import List, Optional
from app.schemas.company import CompanyInfo

class CompanyService:

    def __init__(self):
        
        self._mock_companies = [
            {"company_name": "삼성전자", "ticker": "005930"},
            {"company_name": "삼성전기", "ticker": "005931"},
            {"company_name": "SK하이닉스", "ticker": "000660"},
            {"company_name": "NAVER", "ticker": "035420"},
            {"company_name": "카카오", "ticker": "035720"},
            {"company_name": "현대차", "ticker": "005380"},
        ]
    
    def search_companies(self, keyword: str) -> List[CompanyInfo]:

        if not keyword:
            return []
        
        keyword_lower = keyword.lower()

        results = [
            CompanyInfo(**company)
            for company in self._mock_companies
            if self._matches_keyword(company, keyword_lower)
        ]

        return results
    
    def _matches_keyword(self, company: dict, keyword: str) -> bool:

        company_name = company["company_name"].lower()
        ticker = company["ticker"].lower()

        return keyword in company_name or keyword in ticker


company_service = CompanyService()
