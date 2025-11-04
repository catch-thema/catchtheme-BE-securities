import httpx
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from app.core.config import settings
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

        url = f"{self.base_url}/oauth2/tokenP"
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
                # 토큰은 24시간 유효하지만, 안전하게 23시간으로 설정
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
        url = f"{self.base_url}/uapi/domestic-stock/v1/quotations/inquire-price"

        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": "FHKST01010100"  # 국내주식 현재가 시세 조회
        }

        params = {
            "FID_COND_MRKT_DIV_CODE": "J",  # 시장 구분 코드 (J: 주식)
            "FID_INPUT_ISCD": ticker  # 종목코드
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
        """주식 기본 조회 - 기업 기본 정보"""
        if len(ticker) != 6:
            logger.warning(f"Invalid ticker format: {ticker}")
            return None

        token = self._get_access_token()
        url = f"{self.base_url}/uapi/domestic-stock/v1/quotations/search-stock-info"

        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": "CTPF1002R"
        }

        params = {
            "PRDT_TYPE_CD": "300",
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
        return self._get_finance_data(ticker, "balance-sheet", "FHKST66430100", "대차대조표")

    def get_income_statement(self, ticker: str) -> Optional[Dict[str, Any]]:
        return self._get_finance_data(ticker, "income-statement", "FHKST66430200", "손익계산서")

    def get_financial_ratio(self, ticker: str) -> Optional[Dict[str, Any]]:
        return self._get_finance_data(ticker, "financial-ratio", "FHKST66430300", "재무비율")

    def get_profit_ratio(self, ticker: str) -> Optional[Dict[str, Any]]:
        return self._get_finance_data(ticker, "profit-ratio", "FHKST66430400", "수익성비율")

    def get_stability_ratio(self, ticker: str) -> Optional[Dict[str, Any]]:
        return self._get_finance_data(ticker, "stability-ratio", "FHKST66430600", "안정성비율")

    def get_growth_ratio(self, ticker: str) -> Optional[Dict[str, Any]]:
        return self._get_finance_data(ticker, "growth-ratio", "FHKST66430800", "성장성비율")

    def _get_finance_data(
        self,
        ticker: str,
        endpoint: str,
        tr_id: str,
        data_name: str
    ) -> Optional[Dict[str, Any]]:
        """재무 데이터 조회 공통 메서드"""
        if len(ticker) != 6:
            logger.warning(f"Invalid ticker format: {ticker}")
            return None

        token = self._get_access_token()
        url = f"{self.base_url}/uapi/domestic-stock/v1/finance/{endpoint}"

        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": tr_id
        }

        params = {
            "FID_DIV_CLS_CODE": "1",  # 1: 분기별 데이터 (최신 데이터)
            "fid_cond_mrkt_div_code": "J",
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

                # 빈 리스트 체크
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
