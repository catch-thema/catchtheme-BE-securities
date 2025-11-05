from sqlalchemy import Column, String, Integer, Numeric, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class ExchangeRate(Base):
    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    currency_code = Column(String(10), unique=True, nullable=False, index=True, comment="통화 코드 (예: USD)")
    currency_name = Column(String(50), comment="통화명 (예: 미국 달러)")

    base_rate = Column(Numeric(15, 2), nullable=False, comment="기준율 (매매기준율)")
    previous_rate = Column(Numeric(15, 2), comment="이전 기준율 (등락률 계산용)")
    change_rate = Column(Numeric(10, 4), comment="등락률 (%)")

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="업데이트 시각")
