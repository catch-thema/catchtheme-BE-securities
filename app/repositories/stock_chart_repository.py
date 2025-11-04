from typing import Optional
from app.utils.kis_client import get_kis_client
from app.utils.stock_chart_mapper import StockChartMapper
from app.schemas.stock_chart import StockChartInfo
import logging

logger = logging.getLogger(__name__)


class KISStockChartRepository:

    def __init__(self):
        self.kis_client = get_kis_client()
        self.mapper = StockChartMapper()

    def get_stock_chart(
        self,
        ticker: str,
        start_date: str,
        end_date: str,
        period_div_code: str,
        adjusted_price_type: str = "0"
    ) -> Optional[StockChartInfo]:
        chart_data = self.kis_client.get_period_price(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            period_div_code=period_div_code,
            adjusted_price_type=adjusted_price_type
        )

        if not chart_data:
            logger.warning(f"No chart data returned for ticker: {ticker}")
            return None

        output1 = chart_data.get("output1")
        output2 = chart_data.get("output2", [])

        if not output1 or not output2:
            logger.warning(f"Invalid chart data structure for ticker: {ticker}")
            return None

        return self.mapper.map_to_stock_chart_info(output1, output2)
