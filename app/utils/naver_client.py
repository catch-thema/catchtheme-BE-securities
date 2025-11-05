import httpx
from typing import Optional, Dict, Any
from app.core.config import settings
from app.core.constants import NaverAPIEndpoint, NaverAPIConfig
import logging

logger = logging.getLogger(__name__)

class NaverSearchClient:

    def __init__(self):
        self.base_url = settings.NAVER_SEARCH_BASE_URL
        self.client_id = settings.NAVER_CLIENT_ID
        self.client_secret = settings.NAVER_CLIENT_SECRET

    def search_news(
        self,
        query: str,
        display: int = NaverAPIConfig.DEFAULT_DISPLAY,
        start: int = NaverAPIConfig.DEFAULT_START,
        sort: str = NaverAPIConfig.SORT_DATE
    ) -> Optional[Dict[str, Any]]:

        url = f"{self.base_url}{NaverAPIEndpoint.SEARCH_NEWS}"

        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }

        params = {
            "query": query,
            "display": display,
            "start": start,
            "sort": sort
        }

        try:
            with httpx.Client() as client:
                response = client.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()

                logger.info(f"Successfully fetched news for query: {query}")
                return data

        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch news for query '{query}': {e}")
            return None


_naver_search_client: Optional[NaverSearchClient] = None

def get_naver_search_client() -> NaverSearchClient:
    global _naver_search_client
    if _naver_search_client is None:
        _naver_search_client = NaverSearchClient()
    return _naver_search_client
