import httpx
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from app.core.config import settings
from app.core.constants import KISAPIConfig, KISAPIEndpoint
import logging

logger = logging.getLogger(__name__)

class KISClient:

    def __init__(self):
        self.base_url = settings.KIS_BASE_URL
        self.app_key = settings.KIS_APP_KEY
        self.app_secret = settings.KIS_APP_SECRET
        self._access_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None

    def _is_token_valid(self) -> bool:
        if not self._access_token or not self._token_expires_at:
            return False
        return datetime.now() < self._token_expires_at

    def _get_access_token(self) -> str:
        if self._is_token_valid():
            return self._access_token

        url = f"{self.base_url}{KISAPIEndpoint.OAUTH_TOKEN}"
        headers = {"content-type": "application/json"}
        body = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }

        try:
            with httpx.Client() as client:
                response = client.post(url, json=body, headers=headers)
                response.raise_for_status()
                data = response.json()

                self._access_token = data["access_token"]
                self._token_expires_at = datetime.now() + timedelta(hours=23)

                logger.info("KIS API access token issued successfully")
                return self._access_token

        except httpx.HTTPError as e:
            logger.error(f"Failed to get KIS API access token: {e}")
            raise Exception(f"KIS API 토큰 발급 실패: {str(e)}")

    def get_stock_price_info(self, ticker: str) -> Optional[Dict[str, Any]]:
        if len(ticker) != 6:
            logger.warning(f"Invalid ticker format: {ticker}")
            return None

        token = self._get_access_token()
        url = f"{self.base_url}{KISAPIEndpoint.INQUIRE_PRICE}"

        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": KISAPIConfig.TR_ID_INQUIRE_PRICE
        }

        params = {
            "FID_COND_MRKT_DIV_CODE": KISAPIConfig.MARKET_DIV_CODE_KRX,
            "FID_INPUT_ISCD": ticker
        }

        try:
            with httpx.Client() as client:
                response = client.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("rt_cd") != "0":
                    logger.error(f"KIS API error: {data.get('msg1')}")
                    return None

                logger.info(f"Successfully fetched stock price info for {ticker}")
                return data.get("output")

        except httpx.HTTPError as e:
            logger.error(f"Failed to get stock price info for {ticker}: {e}")
            return None

    def get_stock_basic_info(self, ticker: str) -> Optional[Dict[str, Any]]:
        if len(ticker) != 6:
            logger.warning(f"Invalid ticker format: {ticker}")
            return None

        token = self._get_access_token()
        url = f"{self.base_url}{KISAPIEndpoint.SEARCH_STOCK_INFO}"

        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": KISAPIConfig.TR_ID_SEARCH_STOCK_INFO
        }

        params = {
            "PRDT_TYPE_CD": KISAPIConfig.PRODUCT_TYPE_CODE_STOCK,
            "PDNO": ticker
        }

        try:
            with httpx.Client() as client:
                response = client.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("rt_cd") != "0":
                    logger.warning(f"KIS API stock basic info not available for {ticker}: {data.get('msg1')}")
                    return None

                logger.info(f"Successfully fetched stock basic info for {ticker}")
                return data.get("output")

        except httpx.HTTPError as e:
            logger.warning(f"Failed to get stock basic info for {ticker}: {e}")
            return None

    def get_balance_sheet(self, ticker: str) -> Optional[Dict[str, Any]]:
        return self._get_finance_data(
            ticker,
            KISAPIEndpoint.BALANCE_SHEET,
            KISAPIConfig.TR_ID_BALANCE_SHEET,
            "대차대조표"
        )

    def get_income_statement(self, ticker: str) -> Optional[Dict[str, Any]]:
        return self._get_finance_data(
            ticker,
            KISAPIEndpoint.INCOME_STATEMENT,
            KISAPIConfig.TR_ID_INCOME_STATEMENT,
            "손익계산서"
        )

    def get_financial_ratio(self, ticker: str) -> Optional[Dict[str, Any]]:
        return self._get_finance_data(
            ticker,
            KISAPIEndpoint.FINANCIAL_RATIO,
            KISAPIConfig.TR_ID_FINANCIAL_RATIO,
            "재무비율"
        )

    def get_profit_ratio(self, ticker: str) -> Optional[Dict[str, Any]]:
        return self._get_finance_data(
            ticker,
            KISAPIEndpoint.PROFIT_RATIO,
            KISAPIConfig.TR_ID_PROFIT_RATIO,
            "수익성비율"
        )

    def get_stability_ratio(self, ticker: str) -> Optional[Dict[str, Any]]:
        return self._get_finance_data(
            ticker,
            KISAPIEndpoint.STABILITY_RATIO,
            KISAPIConfig.TR_ID_STABILITY_RATIO,
            "안정성비율"
        )

    def get_growth_ratio(self, ticker: str) -> Optional[Dict[str, Any]]:
        return self._get_finance_data(
            ticker,
            KISAPIEndpoint.GROWTH_RATIO,
            KISAPIConfig.TR_ID_GROWTH_RATIO,
            "성장성비율"
        )

    def get_period_price(
        self,
        ticker: str,
        start_date: str,
        end_date: str,
        period_div_code: str,
        adjusted_price_type: str = KISAPIConfig.ADJUSTED_PRICE_TYPE_ADJUSTED
    ) -> Optional[Dict[str, Any]]:
        if len(ticker) != 6:
            logger.warning(f"Invalid ticker format: {ticker}")
            return None

        token = self._get_access_token()
        url = f"{self.base_url}{KISAPIEndpoint.DAILY_CHART}"

        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": KISAPIConfig.TR_ID_DAILY_CHART
        }

        params = {
            "FID_COND_MRKT_DIV_CODE": KISAPIConfig.MARKET_DIV_CODE_KRX,
            "FID_INPUT_ISCD": ticker,
            "FID_INPUT_DATE_1": start_date,
            "FID_INPUT_DATE_2": end_date,
            "FID_PERIOD_DIV_CODE": period_div_code,
            "FID_ORG_ADJ_PRC": adjusted_price_type
        }

        try:
            with httpx.Client() as client:
                response = client.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("rt_cd") != "0":
                    logger.error(f"KIS API period price error for {ticker}: {data.get('msg1')}")
                    return None

                logger.info(f"Successfully fetched period price data for {ticker}")
                return data

        except httpx.HTTPError as e:
            logger.error(f"Failed to get period price data for {ticker}: {e}")
            return None

    def _get_finance_data(
        self,
        ticker: str,
        endpoint: str,
        tr_id: str,
        data_name: str
    ) -> Optional[Dict[str, Any]]:
        if len(ticker) != 6:
            logger.warning(f"Invalid ticker format: {ticker}")
            return None

        token = self._get_access_token()
        url = f"{self.base_url}{endpoint}"

        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": tr_id
        }

        params = {
            "FID_DIV_CLS_CODE": KISAPIConfig.FID_DIV_CLS_CODE_QUARTERLY,
            "fid_cond_mrkt_div_code": KISAPIConfig.MARKET_DIV_CODE_KRX,
            "fid_input_iscd": ticker
        }

        try:
            with httpx.Client() as client:
                response = client.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("rt_cd") != "0":
                    logger.warning(f"KIS API {data_name} error for {ticker}: rt_cd={data.get('rt_cd')}, msg1={data.get('msg1')}")
                    logger.debug(f"Full response: {data}")
                    return None

                output = data.get("output")
                logger.info(f"Successfully fetched {data_name} for {ticker}, output type: {type(output)}, length: {len(output) if isinstance(output, list) else 'N/A'}")

                if isinstance(output, list) and len(output) == 0:
                    logger.warning(f"{data_name} returned empty list for {ticker}")
                    return None

                return output

        except httpx.HTTPError as e:
            logger.warning(f"Failed to get {data_name} for {ticker}: {e}")
            return None




_kis_client: Optional[KISClient] = None

def get_kis_client() -> KISClient:
    global _kis_client
    if _kis_client is None:
        _kis_client = KISClient()
    return _kis_client
