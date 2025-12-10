from typing import Optional, Dict, Any, List
from app.schemas.stock_chart import StockChartSummary, StockChartDataPoint, StockChartInfo


class StockChartMapper:

    @staticmethod
    def map_summary(output1: Dict[str, Any]) -> StockChartSummary:
        return StockChartSummary(
            previous_day_diff=StockChartMapper._safe_int(output1.get("prdy_vrss")),
            previous_day_diff_sign=output1.get("prdy_vrss_sign"),
            previous_day_change_rate=output1.get("prdy_ctrt"),
            previous_day_close=StockChartMapper._safe_int(output1.get("stck_prdy_clpr")),
            accumulated_volume=StockChartMapper._safe_int(output1.get("acml_vol")),
            accumulated_transaction_amount=StockChartMapper._safe_int(output1.get("acml_tr_pbmn")),
            stock_name=output1.get("hts_kor_isnm"),
            current_price=StockChartMapper._safe_int(output1.get("stck_prpr"))
        )

    @staticmethod
    def map_chart_data_point(data_point: Dict[str, Any]) -> StockChartDataPoint:
        return StockChartDataPoint(
            date=data_point.get("stck_bsop_date", ""),
            close_price=StockChartMapper._safe_int(data_point.get("stck_clpr")) or 0,
            open_price=StockChartMapper._safe_int(data_point.get("stck_oprc")) or 0,
            high_price=StockChartMapper._safe_int(data_point.get("stck_hgpr")) or 0,
            low_price=StockChartMapper._safe_int(data_point.get("stck_lwpr")) or 0,
            volume=StockChartMapper._safe_int(data_point.get("acml_vol")) or 0,
            transaction_amount=StockChartMapper._safe_int(data_point.get("acml_tr_pbmn")) or 0
        )

    @staticmethod
    def map_to_stock_chart_info(
        output1: Dict[str, Any],
        output2: List[Dict[str, Any]]
    ) -> StockChartInfo:
        summary = StockChartMapper.map_summary(output1)
        chart_data = [
            StockChartMapper.map_chart_data_point(data_point)
            for data_point in output2
        ]

        return StockChartInfo(
            summary=summary,
            chart_data=chart_data
        )

    @staticmethod
    def _safe_int(value: any) -> Optional[int]:
        if value is None or value == "":
            return None
        try:
            if isinstance(value, str):
                value = value.replace(",", "")
            return int(float(value))
        except (ValueError, TypeError):
            return None
