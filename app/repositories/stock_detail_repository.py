from typing import Optional
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from app.schemas.stock_detail import StockDetailInfo
from app.utils.kis_client import get_kis_client
from app.utils.stock_mapper import StockDataMapper
from app.models.stock_detail import StockPrice, StockCompanyInfo, StockFinancial, StockRatios


class StockDetailRepositoryInterface(ABC):

    @abstractmethod
    def get_stock_detail(self, ticker: str, db: Optional[Session] = None) -> Optional[StockDetailInfo]:
        pass


class KISStockDetailRepository(StockDetailRepositoryInterface):

    def __init__(self):
        self.kis_client = get_kis_client()
        self.mapper = StockDataMapper()

    def get_stock_detail(self, ticker: str, db: Optional[Session] = None) -> Optional[StockDetailInfo]:
        """
        종목 상세 정보 조회 - 8개의 KIS API 호출

        1. inquire-price: 현재가 및 시세 정보
        2. search-stock-info: 기업 기본 정보
        3. balance-sheet: 대차대조표
        4. income-statement: 손익계산서
        5. financial-ratio: 재무비율
        6. profit-ratio: 수익성비율
        7. stability-ratio: 안정성비율
        8. growth-ratio: 성장성비율
        """

        # 1. 필수: 현재가 정보 (이게 없으면 종목이 존재하지 않음)
        price_data = self.kis_client.get_stock_price_info(ticker)
        if not price_data:
            return None

        # 2-8. 선택적: 추가 정보 (실패해도 계속 진행)
        basic_data = self.kis_client.get_stock_basic_info(ticker)
        balance_data = self.kis_client.get_balance_sheet(ticker)
        income_data = self.kis_client.get_income_statement(ticker)
        financial_data = self.kis_client.get_financial_ratio(ticker)
        profit_data = self.kis_client.get_profit_ratio(ticker)
        stability_data = self.kis_client.get_stability_ratio(ticker)
        growth_data = self.kis_client.get_growth_ratio(ticker)

        # 매퍼를 사용하여 스키마 객체로 변환
        stock_detail = self.mapper.map_to_stock_detail_info(
            price_data=price_data,
            basic_data=basic_data,
            balance_data=balance_data,
            income_data=income_data,
            financial_data=financial_data,
            profit_data=profit_data,
            stability_data=stability_data,
            growth_data=growth_data
        )

        # DB에 저장 (Session이 제공된 경우)
        if db is not None and stock_detail is not None:
            self._save_to_db(db, ticker, stock_detail)

        return stock_detail

    def _save_to_db(self, db: Session, ticker: str, stock_detail: StockDetailInfo):
        """종목 상세 정보를 DB에 저장"""
        try:
            # 1. 가격 정보 저장
            if stock_detail.price:
                self._save_price_info(db, ticker, stock_detail.price)

            # 2. 기업 정보 저장
            if stock_detail.company:
                self._save_company_info(db, ticker, stock_detail.company)

            # 3. 재무 정보 저장 (재무상태표 + 손익계산서)
            if stock_detail.financial_position or stock_detail.income_statement:
                self._save_financial_info(
                    db, ticker,
                    stock_detail.financial_position,
                    stock_detail.income_statement
                )

            # 4. 비율 정보 저장 (재무비율 + 수익성 + 안정성 + 성장성)
            if any([stock_detail.financial_ratios, stock_detail.profitability,
                    stock_detail.stability, stock_detail.growth]):
                self._save_ratios_info(
                    db, ticker,
                    stock_detail.financial_ratios,
                    stock_detail.profitability,
                    stock_detail.stability,
                    stock_detail.growth
                )

            db.commit()
        except Exception as e:
            db.rollback()
            raise e

    def _save_price_info(self, db: Session, ticker: str, price_info):
        """가격 정보 저장"""
        # 기존 데이터 삭제 후 새로 삽입 (최신 데이터 유지)
        db.query(StockPrice).filter(StockPrice.ticker == ticker).delete()

        price_model = StockPrice(
            ticker=ticker,
            current_price=price_info.current_price,
            opening_price=price_info.opening_price,
            high_price=price_info.high_price,
            low_price=price_info.low_price,
            volume=price_info.volume,
            transaction_amount=price_info.transaction_amount,
            market_cap=price_info.market_cap,
            per=price_info.per,
            pbr=price_info.pbr
        )
        db.add(price_model)

    def _save_company_info(self, db: Session, ticker: str, company_info):
        """기업 정보 저장 (upsert)"""
        existing = db.query(StockCompanyInfo).filter(StockCompanyInfo.ticker == ticker).first()

        if existing:
            # 업데이트
            existing.settlement_month = company_info.settlement_month
            existing.listed_shares = company_info.listed_shares
            existing.listed_capital = company_info.listed_capital
            existing.capital = company_info.capital
            existing.par_value = company_info.par_value
            existing.previous_close = company_info.previous_close
            existing.close_price_change_date = company_info.close_price_change_date
        else:
            # 새로 삽입
            company_model = StockCompanyInfo(
                ticker=ticker,
                settlement_month=company_info.settlement_month,
                listed_shares=company_info.listed_shares,
                listed_capital=company_info.listed_capital,
                capital=company_info.capital,
                par_value=company_info.par_value,
                previous_close=company_info.previous_close,
                close_price_change_date=company_info.close_price_change_date
            )
            db.add(company_model)

    def _save_financial_info(self, db: Session, ticker: str, balance_info, income_info):
        """재무 정보 저장 (재무상태표 + 손익계산서)"""
        fiscal_year_month = None
        if balance_info:
            fiscal_year_month = balance_info.fiscal_year_month
        elif income_info:
            fiscal_year_month = income_info.fiscal_year_month

        if not fiscal_year_month:
            return

        # 같은 결산년월 데이터가 있으면 업데이트, 없으면 삽입
        existing = db.query(StockFinancial).filter(
            StockFinancial.ticker == ticker,
            StockFinancial.fiscal_year_month == fiscal_year_month
        ).first()

        if existing:
            # 업데이트
            if balance_info:
                existing.current_assets = balance_info.current_assets
                existing.fixed_assets = balance_info.fixed_assets
                existing.total_assets = balance_info.total_assets
                existing.current_liabilities = balance_info.current_liabilities
                existing.fixed_liabilities = balance_info.fixed_liabilities
                existing.total_liabilities = balance_info.total_liabilities
                existing.capital_surplus = balance_info.capital_surplus
                existing.retained_earnings = balance_info.retained_earnings
                existing.total_equity = balance_info.total_equity
            if income_info:
                existing.revenue = income_info.revenue
                existing.cost_of_sales = income_info.cost_of_sales
                existing.gross_profit = income_info.gross_profit
                existing.net_income = income_info.net_income
        else:
            # 새로 삽입
            financial_model = StockFinancial(
                ticker=ticker,
                fiscal_year_month=fiscal_year_month,
                current_assets=balance_info.current_assets if balance_info else None,
                fixed_assets=balance_info.fixed_assets if balance_info else None,
                total_assets=balance_info.total_assets if balance_info else None,
                current_liabilities=balance_info.current_liabilities if balance_info else None,
                fixed_liabilities=balance_info.fixed_liabilities if balance_info else None,
                total_liabilities=balance_info.total_liabilities if balance_info else None,
                capital_surplus=balance_info.capital_surplus if balance_info else None,
                retained_earnings=balance_info.retained_earnings if balance_info else None,
                total_equity=balance_info.total_equity if balance_info else None,
                revenue=income_info.revenue if income_info else None,
                cost_of_sales=income_info.cost_of_sales if income_info else None,
                gross_profit=income_info.gross_profit if income_info else None,
                net_income=income_info.net_income if income_info else None
            )
            db.add(financial_model)

    def _save_ratios_info(self, db: Session, ticker: str, financial_ratios, profitability, stability, growth):
        """비율 정보 저장"""
        fiscal_year_month = None
        if financial_ratios:
            fiscal_year_month = financial_ratios.fiscal_year_month
        elif profitability:
            fiscal_year_month = profitability.fiscal_year_month
        elif stability:
            fiscal_year_month = stability.fiscal_year_month
        elif growth:
            fiscal_year_month = growth.fiscal_year_month

        if not fiscal_year_month:
            return

        # 같은 결산년월 데이터가 있으면 업데이트, 없으면 삽입
        existing = db.query(StockRatios).filter(
            StockRatios.ticker == ticker,
            StockRatios.fiscal_year_month == fiscal_year_month
        ).first()

        if existing:
            # 업데이트
            if financial_ratios:
                existing.revenue_growth_rate = financial_ratios.revenue_growth_rate
                existing.operating_profit_growth_rate = financial_ratios.operating_profit_growth_rate
                existing.net_income_growth_rate = financial_ratios.net_income_growth_rate
                existing.roe = financial_ratios.roe
                existing.eps = financial_ratios.eps
                existing.sps = financial_ratios.sps
                existing.bps = financial_ratios.bps
                existing.retention_ratio = financial_ratios.retention_ratio
                existing.debt_ratio = financial_ratios.debt_ratio
            if profitability:
                existing.return_on_assets = profitability.return_on_assets
                existing.return_on_equity = profitability.return_on_equity
                existing.net_profit_margin = profitability.net_profit_margin
                existing.gross_profit_margin = profitability.gross_profit_margin
            if stability:
                existing.stability_debt_ratio = stability.debt_ratio
                existing.borrowing_dependency = stability.borrowing_dependency
                existing.current_ratio = stability.current_ratio
                existing.quick_ratio = stability.quick_ratio
            if growth:
                existing.equity_growth_rate = growth.equity_growth_rate
                existing.total_assets_growth_rate = growth.total_assets_growth_rate
        else:
            # 새로 삽입
            ratios_model = StockRatios(
                ticker=ticker,
                fiscal_year_month=fiscal_year_month,
                revenue_growth_rate=financial_ratios.revenue_growth_rate if financial_ratios else None,
                operating_profit_growth_rate=financial_ratios.operating_profit_growth_rate if financial_ratios else None,
                net_income_growth_rate=financial_ratios.net_income_growth_rate if financial_ratios else None,
                roe=financial_ratios.roe if financial_ratios else None,
                eps=financial_ratios.eps if financial_ratios else None,
                sps=financial_ratios.sps if financial_ratios else None,
                bps=financial_ratios.bps if financial_ratios else None,
                retention_ratio=financial_ratios.retention_ratio if financial_ratios else None,
                debt_ratio=financial_ratios.debt_ratio if financial_ratios else None,
                return_on_assets=profitability.return_on_assets if profitability else None,
                return_on_equity=profitability.return_on_equity if profitability else None,
                net_profit_margin=profitability.net_profit_margin if profitability else None,
                gross_profit_margin=profitability.gross_profit_margin if profitability else None,
                stability_debt_ratio=stability.debt_ratio if stability else None,
                borrowing_dependency=stability.borrowing_dependency if stability else None,
                current_ratio=stability.current_ratio if stability else None,
                quick_ratio=stability.quick_ratio if stability else None,
                equity_growth_rate=growth.equity_growth_rate if growth else None,
                total_assets_growth_rate=growth.total_assets_growth_rate if growth else None
            )
            db.add(ratios_model)
