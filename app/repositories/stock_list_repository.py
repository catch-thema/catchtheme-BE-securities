from typing import List, Optional
from app.utils.krx_client import get_krx_client
from app.schemas.stock_list import StockInfo
import logging

logger = logging.getLogger(__name__)


class KRXStockListRepository:

    def __init__(self):
        self.krx_client = get_krx_client()

    def get_all_stocks(self) -> Optional[List[StockInfo]]:
        try:
            stocks_data = self.krx_client.get_all_stocks()

            if not stocks_data:
                logger.warning("No stocks data received from KRX")
                return None

            stocks = [StockInfo(**stock_data) for stock_data in stocks_data]

            logger.info(f"Successfully retrieved {len(stocks)} stocks from KRX")
            return stocks

        except Exception as e:
            logger.error(f"Failed to get all stocks: {e}")
            raise
