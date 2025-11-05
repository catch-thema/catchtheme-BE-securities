import logging
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
from app.models.exchange_rate import ExchangeRate
from app.schemas.exchange_rate import ExchangeRateData
from app.utils.koreaexim_client import get_koreaexim_client
from app.utils.exchange_rate_mapper import ExchangeRateMapper

logger = logging.getLogger(__name__)

class ExchangeRateRepository:
    def __init__(self):
        self.client = get_koreaexim_client()
        self.mapper = ExchangeRateMapper()

    def get_usd_exchange_rate(self, db: Session) -> Optional[ExchangeRateData]:
        db_rate = db.query(ExchangeRate).filter(
            ExchangeRate.currency_code == "USD"
        ).first()

        if db_rate:
            return ExchangeRateData(
                base_rate=db_rate.base_rate,
                change_rate=db_rate.change_rate
            )

        return None

    def update_usd_exchange_rate(self, db: Session) -> Optional[ExchangeRateData]:
        api_data = self.client.get_usd_exchange_rate()

        if not api_data:
            logger.error("Failed to fetch USD exchange rate from API")
            return None

        rate_data = self.mapper.map_to_schema(api_data)

        existing_rate = db.query(ExchangeRate).filter(
            ExchangeRate.currency_code == "USD"
        ).first()

        if existing_rate:
            previous_rate = existing_rate.base_rate
            change_rate = self._calculate_change_rate(previous_rate, rate_data.base_rate)

            existing_rate.currency_name = api_data.get("cur_nm")
            existing_rate.base_rate = rate_data.base_rate
            existing_rate.previous_rate = previous_rate
            existing_rate.change_rate = change_rate
        else:
            existing_rate = ExchangeRate(
                currency_code="USD",
                currency_name=api_data.get("cur_nm"),
                base_rate=rate_data.base_rate,
                previous_rate=rate_data.base_rate,
                change_rate=Decimal("0")
            )
            db.add(existing_rate)

        try:
            db.commit()
            db.refresh(existing_rate)

            return ExchangeRateData(
                base_rate=existing_rate.base_rate,
                change_rate=existing_rate.change_rate
            )
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update exchange rate: {str(e)}")
            return None

    def _calculate_change_rate(self, previous_rate: Decimal, current_rate: Decimal) -> Decimal:
        if previous_rate == 0:
            return Decimal("0")

        change = ((current_rate - previous_rate) / previous_rate) * 100
        return change.quantize(Decimal("0.0001"))
