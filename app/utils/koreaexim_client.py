import httpx
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from app.core.config import settings
from app.core.constants import KoreaEximAPIConfig, KoreaEximAPIEndpoint

logger = logging.getLogger(__name__)

class KoreaEximClient:
    def __init__(self):
        self.base_url = settings.KOREAEXIM_BASE_URL
        self.api_key = settings.KOREAEXIM_API_KEY

    def get_exchange_rates(self, search_date: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        if not search_date:
            search_date = datetime.now().strftime("%Y%m%d")

        url = f"{self.base_url}{KoreaEximAPIEndpoint.EXCHANGE_RATE_JSON}"

        params = {
            "authkey": self.api_key,
            "searchdate": search_date,
            "data": KoreaEximAPIConfig.DATA_TYPE_AP01
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.get(url, params=params)
                response.raise_for_status()

                data = response.json()

                if not isinstance(data, list):
                    logger.error(f"Unexpected response format: {data}")
                    return None

                return data

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None

    def get_usd_exchange_rate(self, search_date: Optional[str] = None) -> Optional[Dict[str, Any]]:
        exchange_rates = self.get_exchange_rates(search_date)

        if not exchange_rates:
            return None

        for rate in exchange_rates:
            if rate.get("cur_unit") == KoreaEximAPIConfig.CURRENCY_CODE_USD:
                return rate

        logger.warning("USD exchange rate not found in response")
        return None

_koreaexim_client: Optional[KoreaEximClient] = None

def get_koreaexim_client() -> KoreaEximClient:
    global _koreaexim_client
    if _koreaexim_client is None:
        _koreaexim_client = KoreaEximClient()
    return _koreaexim_client
