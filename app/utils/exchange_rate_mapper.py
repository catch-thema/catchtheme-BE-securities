from decimal import Decimal, InvalidOperation
from typing import Dict, Any, Optional
from app.schemas.exchange_rate import ExchangeRateData

class ExchangeRateMapper:
    @staticmethod
    def map_to_schema(data: Dict[str, Any]) -> ExchangeRateData:
        return ExchangeRateData(
            base_rate=ExchangeRateMapper._safe_decimal(data.get("deal_bas_r")),
            change_rate=None
        )

    @staticmethod
    def _safe_decimal(value: Any) -> Optional[Decimal]:
        if value is None or value == "":
            return None

        try:
            if isinstance(value, str):
                value = value.replace(",", "")
            return Decimal(str(value))
        except (ValueError, TypeError, InvalidOperation):
            return None
