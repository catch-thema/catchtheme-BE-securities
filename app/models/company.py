from sqlalchemy import Column, String, Integer, BigInteger, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticker = Column(String(20), unique=True, nullable=False, index=True, comment="종목 코드")
    company_name = Column(String(255), nullable=False, index=True, comment="기업명")

    stock_info = relationship("StockInfo", back_populates="company", uselist=False, cascade="all, delete-orphan")


class StockInfo(Base):
    __tablename__ = "stock_info"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), unique=True, nullable=False)
    ticker = Column(String(20), unique=True, nullable=False, index=True, comment="종목 코드 (중복 저장)")

    current_price = Column(Integer, comment="현재가")
    opening_price = Column(Integer, comment="시가")
    high_price = Column(Integer, comment="고가")
    low_price = Column(Integer, comment="저가")
    previous_close = Column(Integer, comment="전이리 종가")

    volume = Column(BigInteger, comment="거래량")
    transaction_amount = Column(BigInteger, comment="거래대금")

    market_cap = Column(BigInteger, comment="시가총액")
    per = Column(Numeric(10, 2), comment="PER (주가수익비율)")
    pbr = Column(Numeric(10, 2), comment="PBR (주가순자산비율)")
    roe = Column(Numeric(10, 2), comment="ROE (자기자본이익률)")
    psr = Column(Numeric(10, 2), comment="PSR (주가매출비율)")
    dividend_yield = Column(Numeric(10, 2), comment="배당수익률")

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    company = relationship("Company", back_populates="stock_info")
