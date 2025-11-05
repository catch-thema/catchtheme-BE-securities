from sqlalchemy import Column, String, Numeric, DateTime, Integer
from sqlalchemy.sql import func
from app.db.base import Base


class MarketIndex(Base):
    __tablename__ = "market_indices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(20), unique=True, nullable=False, index=True, comment="지수 코드 (0001, 1001, NAS, SPX)")
    name = Column(String(50), nullable=False, comment="지수명 (KOSPI, KOSDAQ, NASDAQ, SP500)")
    current_price = Column(Numeric(20, 2), nullable=False, comment="현재가")
    change_rate = Column(Numeric(10, 2), nullable=False, comment="등락률 (%)")
    change_price = Column(Numeric(20, 2), nullable=False, comment="전일대비")
    timestamp = Column(String(20), nullable=False, comment="데이터 시간")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="DB 업데이트 시간")
