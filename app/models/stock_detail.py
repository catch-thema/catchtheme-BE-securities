from sqlalchemy import Column, String, Integer, BigInteger, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class StockPrice(Base):
    """주식 가격 및 거래 정보"""
    __tablename__ = "stock_price"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticker = Column(String(20), nullable=False, index=True, comment="종목 코드")

    # 가격 정보
    current_price = Column(Integer, comment="현재가")
    opening_price = Column(Integer, comment="시가")
    high_price = Column(Integer, comment="고가")
    low_price = Column(Integer, comment="저가")

    # 거래 정보
    volume = Column(BigInteger, comment="거래량")
    transaction_amount = Column(BigInteger, comment="거래대금")

    # 평가 정보
    market_cap = Column(BigInteger, comment="시가총액")
    per = Column(Numeric(10, 2), comment="PER (주가수익비율)")
    pbr = Column(Numeric(10, 2), comment="PBR (주가순자산비율)")

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class StockCompanyInfo(Base):
    """기업 기본 정보"""
    __tablename__ = "stock_company_info"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticker = Column(String(20), unique=True, nullable=False, index=True, comment="종목 코드")

    settlement_month = Column(String(10), comment="결산월일")
    listed_shares = Column(BigInteger, comment="상장주수")
    listed_capital = Column(BigInteger, comment="상장자본금액")
    capital = Column(BigInteger, comment="자본금")
    par_value = Column(Integer, comment="액면가")
    previous_close = Column(Integer, comment="전일종가")
    close_price_change_date = Column(String(10), comment="종가변경일자")

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class StockFinancial(Base):
    """재무상태표 + 손익계산서"""
    __tablename__ = "stock_financial"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticker = Column(String(20), nullable=False, index=True, comment="종목 코드")
    fiscal_year_month = Column(String(10), comment="결산년월")

    # 재무상태표 (대차대조표)
    current_assets = Column(BigInteger, comment="유동자산")
    fixed_assets = Column(BigInteger, comment="고정자산")
    total_assets = Column(BigInteger, comment="자산총계")
    current_liabilities = Column(BigInteger, comment="유동부채")
    fixed_liabilities = Column(BigInteger, comment="고정부채")
    total_liabilities = Column(BigInteger, comment="부채총계")
    capital_surplus = Column(BigInteger, comment="자본잉여금")
    retained_earnings = Column(BigInteger, comment="이익잉여금")
    total_equity = Column(BigInteger, comment="자본총계")

    # 손익계산서
    revenue = Column(BigInteger, comment="매출액")
    cost_of_sales = Column(BigInteger, comment="매출원가")
    gross_profit = Column(BigInteger, comment="매출총이익")
    net_income = Column(BigInteger, comment="당기순이익")

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class StockRatios(Base):
    """재무비율 + 수익성 + 안정성 + 성장성"""
    __tablename__ = "stock_ratios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticker = Column(String(20), nullable=False, index=True, comment="종목 코드")
    fiscal_year_month = Column(String(10), comment="결산년월")

    # 재무비율
    revenue_growth_rate = Column(Numeric(10, 2), comment="매출액증가율")
    operating_profit_growth_rate = Column(Numeric(10, 2), comment="영업이익증가율")
    net_income_growth_rate = Column(Numeric(10, 2), comment="순이익증가율")
    roe = Column(Numeric(10, 2), comment="ROE (자기자본이익률)")
    eps = Column(Numeric(10, 2), comment="EPS (주당순이익)")
    sps = Column(Numeric(10, 2), comment="주당매출액")
    bps = Column(Numeric(10, 2), comment="BPS (주당순자산)")
    retention_ratio = Column(Numeric(10, 2), comment="유보비율")
    debt_ratio = Column(Numeric(10, 2), comment="부채비율")

    # 수익성비율
    return_on_assets = Column(Numeric(10, 2), comment="총자본순이익률 (ROA)")
    return_on_equity = Column(Numeric(10, 2), comment="자기자본순이익률")
    net_profit_margin = Column(Numeric(10, 2), comment="매출액순이익률")
    gross_profit_margin = Column(Numeric(10, 2), comment="매출액총이익률")

    # 안정성비율
    stability_debt_ratio = Column(Numeric(10, 2), comment="부채비율")
    borrowing_dependency = Column(Numeric(10, 2), comment="차입금의존도")
    current_ratio = Column(Numeric(10, 2), comment="유동비율")
    quick_ratio = Column(Numeric(10, 2), comment="당좌비율")

    # 성장성비율
    equity_growth_rate = Column(Numeric(10, 2), comment="자기자본증가율")
    total_assets_growth_rate = Column(Numeric(10, 2), comment="총자산증가율")

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
