import httpx
import csv
from io import StringIO
from typing import List, Dict, Any, Optional
from app.core.constants import KRXAPIConfig, ErrorMessage
import logging

logger = logging.getLogger(__name__)


class KRXClient:

    def __init__(self):
        self.base_url = KRXAPIConfig.BASE_URL
        self.generate_otp_url = f"{self.base_url}{KRXAPIConfig.GENERATE_OTP_PATH}"
        self.download_csv_url = f"{self.base_url}{KRXAPIConfig.DOWNLOAD_CSV_PATH}"
        self.referer = KRXAPIConfig.REFERER

    def _generate_otp(self) -> Optional[str]:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "data.krx.co.kr",
            "Referer": self.referer,
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": KRXAPIConfig.USER_AGENT
        }

        params = {
            "locale": KRXAPIConfig.LOCALE,
            "mktId": KRXAPIConfig.MARKET_ID_ALL,
            "share": KRXAPIConfig.SHARE,
            "csvxls_isNo": KRXAPIConfig.CSVXLS_IS_NO,
            "name": KRXAPIConfig.FILE_DOWN_NAME,
            "url": KRXAPIConfig.STOCK_INFO_URL
        }

        try:
            with httpx.Client(follow_redirects=True) as client:
                response = client.get(
                    self.generate_otp_url,
                    params=params,
                    headers=headers,
                    timeout=30.0
                )
                response.raise_for_status()
                otp_code = response.text.strip()

                if not otp_code:
                    logger.error("OTP code is empty")
                    return None

                logger.info("KRX OTP generated successfully")
                return otp_code

        except httpx.HTTPError as e:
            logger.error(f"Failed to generate KRX OTP: {e}")
            return None

    def _download_csv(self, otp_code: str) -> Optional[str]:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "data.krx.co.kr",
            "Origin": "https://data.krx.co.kr",
            "Referer": self.referer,
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": KRXAPIConfig.USER_AGENT
        }

        payload = {
            "code": otp_code
        }

        try:
            with httpx.Client(follow_redirects=True) as client:
                response = client.post(
                    self.download_csv_url,
                    data=payload,
                    headers=headers,
                    timeout=30.0
                )
                response.raise_for_status()

                csv_content = response.content.decode(KRXAPIConfig.ENCODING)

                if not csv_content or len(csv_content) < 100:
                    logger.error("Downloaded CSV content is empty or too short")
                    return None

                logger.info(f"KRX CSV downloaded successfully, size: {len(csv_content)} bytes")
                return csv_content

        except (httpx.HTTPError, UnicodeDecodeError) as e:
            logger.error(f"Failed to download KRX CSV: {e}")
            return None

    def _parse_csv(self, csv_content: str) -> List[Dict[str, Any]]:
        try:
            csv_file = StringIO(csv_content)
            reader = csv.DictReader(csv_file)

            stocks = []
            for row in reader:
                stock = {
                    "standard_code": row.get("표준코드", "").strip(),
                    "short_code": row.get("단축코드", "").strip(),
                    "korean_name": row.get("한글 종목명", "").strip(),
                    "korean_short_name": row.get("한글 종목약명", "").strip(),
                    "english_name": row.get("영문 종목명", "").strip(),
                    "listing_date": row.get("상장일", "").strip(),
                    "market_type": row.get("시장구분", "").strip(),
                    "security_type": row.get("증권구분", "").strip(),
                    "sector": row.get("소속부", "").strip(),
                    "stock_type": row.get("주식종류", "").strip(),
                    "par_value": self._parse_number(row.get("액면가", "")),
                    "listed_shares": self._parse_number(row.get("상장주식수", ""))
                }
                stocks.append(stock)

            logger.info(f"Parsed {len(stocks)} stocks from CSV")
            return stocks

        except Exception as e:
            logger.error(f"Failed to parse CSV: {e}")
            raise Exception(ErrorMessage.KRX_CSV_PARSE_FAILED)

    def _parse_number(self, value: str) -> Optional[int]:
        if not value or value.strip() == "":
            return None
        try:
            cleaned = value.replace(",", "").strip()
            return int(cleaned) if cleaned else None
        except (ValueError, AttributeError):
            return None

    def get_all_stocks(self) -> List[Dict[str, Any]]:
        otp_code = self._generate_otp()
        if not otp_code:
            raise Exception(ErrorMessage.KRX_OTP_GENERATION_FAILED)

        csv_content = self._download_csv(otp_code)
        if not csv_content:
            raise Exception(ErrorMessage.KRX_CSV_DOWNLOAD_FAILED)

        stocks = self._parse_csv(csv_content)
        return stocks


_krx_client: Optional[KRXClient] = None

def get_krx_client() -> KRXClient:
    global _krx_client
    if _krx_client is None:
        _krx_client = KRXClient()
    return _krx_client
