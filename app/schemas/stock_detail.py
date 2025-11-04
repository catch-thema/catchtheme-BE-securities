from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class PriceInfo(BaseModel):
    """가격 및 거래 정보 (inquire-price API)"""
    current_price: Optional[int] = Field(None, description="현재가")
    opening_price: Optional[int] = Field(None, description="시가")
    high_price: Optional[int] = Field(None, description="고가")
    low_price: Optional[int] = Field(None, description="저가")
    volume: Optional[int] = Field(None, description="거래량")
    transaction_amount: Optional[int] = Field(None, description="거래대금")
    market_cap: Optional[int] = Field(None, description="시가총액")
    per: Optional[Decimal] = Field(None, description="PER (주가수익비율)")
    pbr: Optional[Decimal] = Field(None, description="PBR (주가순자산비율)")


class CompanyInfo(BaseModel):
    """기업 기본 정보 (search-stock-info API)"""
    settlement_month: Optional[str] = Field(None, description="결산월일")
    listed_shares: Optional[int] = Field(None, description="상장주수")
    listed_capital: Optional[int] = Field(None, description="상장자본금액")
    capital: Optional[int] = Field(None, description="자본금")
    par_value: Optional[int] = Field(None, description="액면가")
    previous_close: Optional[int] = Field(None, description="전일종가")
    close_price_change_date: Optional[str] = Field(None, description="종가변경일자")


class FinancialPosition(BaseModel):
    """재무상태표 (대차대조표)"""
    fiscal_year_month: Optional[str] = Field(None, description="결산년월")
    current_assets: Optional[int] = Field(None, description="유동자산")
    fixed_assets: Optional[int] = Field(None, description="고정자산")
    total_assets: Optional[int] = Field(None, description="자산총계")
    current_liabilities: Optional[int] = Field(None, description="유동부채")
    fixed_liabilities: Optional[int] = Field(None, description="고정부채")
    total_liabilities: Optional[int] = Field(None, description="부채총계")
    capital_surplus: Optional[int] = Field(None, description="자본잉여금")
    retained_earnings: Optional[int] = Field(None, description="이익잉여금")
    total_equity: Optional[int] = Field(None, description="자본총계")


class IncomeStatement(BaseModel):
    """손익계산서"""
    fiscal_year_month: Optional[str] = Field(None, description="결산년월")
    revenue: Optional[int] = Field(None, description="매출액")
    cost_of_sales: Optional[int] = Field(None, description="매출원가")
    gross_profit: Optional[int] = Field(None, description="매출총이익")
    net_income: Optional[int] = Field(None, description="당기순이익")


class FinancialRatios(BaseModel):
    """재무비율 (financial-ratio API)"""
    fiscal_year_month: Optional[str] = Field(None, description="결산년월")
    revenue_growth_rate: Optional[Decimal] = Field(None, description="매출액증가율")
    operating_profit_growth_rate: Optional[Decimal] = Field(None, description="영업이익증가율")
    net_income_growth_rate: Optional[Decimal] = Field(None, description="순이익증가율")
    roe: Optional[Decimal] = Field(None, description="ROE (자기자본이익률)")
    eps: Optional[Decimal] = Field(None, description="EPS (주당순이익)")
    sps: Optional[Decimal] = Field(None, description="주당매출액")
    bps: Optional[Decimal] = Field(None, description="BPS (주당순자산)")
    retention_ratio: Optional[Decimal] = Field(None, description="유보비율")
    debt_ratio: Optional[Decimal] = Field(None, description="부채비율")


class ProfitabilityRatios(BaseModel):
    """수익성비율 (profit-ratio API)"""
    fiscal_year_month: Optional[str] = Field(None, description="결산년월")
    return_on_assets: Optional[Decimal] = Field(None, description="총자본순이익률 (ROA)")
    return_on_equity: Optional[Decimal] = Field(None, description="자기자본순이익률")
    net_profit_margin: Optional[Decimal] = Field(None, description="매출액순이익률")
    gross_profit_margin: Optional[Decimal] = Field(None, description="매출액총이익률")


class StabilityRatios(BaseModel):
    """안정성비율 (stability-ratio API)"""
    fiscal_year_month: Optional[str] = Field(None, description="결산년월")
    debt_ratio: Optional[Decimal] = Field(None, description="부채비율")
    borrowing_dependency: Optional[Decimal] = Field(None, description="차입금의존도")
    current_ratio: Optional[Decimal] = Field(None, description="유동비율")
    quick_ratio: Optional[Decimal] = Field(None, description="당좌비율")


class GrowthRatios(BaseModel):
    """성장성비율 (growth-ratio API)"""
    fiscal_year_month: Optional[str] = Field(None, description="결산년월")
    revenue_growth_rate: Optional[Decimal] = Field(None, description="매출액증가율")
    operating_profit_growth_rate: Optional[Decimal] = Field(None, description="영업이익증가율")
    equity_growth_rate: Optional[Decimal] = Field(None, description="자기자본증가율")
    total_assets_growth_rate: Optional[Decimal] = Field(None, description="총자산증가율")


class StockDetailInfo(BaseModel):
    """종목 상세 정보 - API별 그룹화"""
    price: PriceInfo = Field(..., description="가격 및 거래 정보")
    company: Optional[CompanyInfo] = Field(None, description="기업 기본 정보")
    financial_position: Optional[FinancialPosition] = Field(None, description="재무상태표")
    income_statement: Optional[IncomeStatement] = Field(None, description="손익계산서")
    financial_ratios: Optional[FinancialRatios] = Field(None, description="재무비율")
    profitability: Optional[ProfitabilityRatios] = Field(None, description="수익성비율")
    stability: Optional[StabilityRatios] = Field(None, description="안정성비율")
    growth: Optional[GrowthRatios] = Field(None, description="성장성비율")

    class Config:
        from_attributes = True


class StockDetailResponse(BaseModel):
    """종목 상세 정보 응답"""
    status: int
    message: str
    data: Optional[StockDetailInfo] = None
