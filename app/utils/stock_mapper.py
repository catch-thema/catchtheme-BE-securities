from typing import Optional, Union, List, Dict, Any
from decimal import Decimal

from app.schemas.stock_detail import (
    PriceInfo, CompanyInfo, FinancialPosition, IncomeStatement,
    FinancialRatios, ProfitabilityRatios, StabilityRatios,
    GrowthRatios, StockDetailInfo
)


class StockDataMapper:

    @staticmethod
    def map_price_info(price_data: Dict[str, Any]) -> PriceInfo:
        return PriceInfo(
            current_price=StockDataMapper._safe_int(price_data.get("stck_prpr")),
            opening_price=StockDataMapper._safe_int(price_data.get("stck_oprc")),
            high_price=StockDataMapper._safe_int(price_data.get("stck_hgpr")),
            low_price=StockDataMapper._safe_int(price_data.get("stck_lwpr")),
            volume=StockDataMapper._safe_int(price_data.get("acml_vol")),
            transaction_amount=StockDataMapper._safe_int(price_data.get("acml_tr_pbmn")),
            market_cap=StockDataMapper._safe_int(price_data.get("hts_avls")),
            per=StockDataMapper._safe_decimal(price_data.get("per")),
            pbr=StockDataMapper._safe_decimal(price_data.get("pbr"))
        )

    @staticmethod
    def map_company_info(basic_data: Optional[Dict[str, Any]]) -> Optional[CompanyInfo]:
        """기업 기본 정보 매핑 (search-stock-info API) - dict 형태로 반환"""
        if not basic_data:
            return None

        return CompanyInfo(
            settlement_month=basic_data.get("setl_mmdd"),
            listed_shares=StockDataMapper._safe_int(basic_data.get("lstg_stqt")),
            listed_capital=StockDataMapper._safe_int(basic_data.get("lstg_cptl_amt")),
            capital=StockDataMapper._safe_int(basic_data.get("cpta")),
            par_value=StockDataMapper._safe_int(basic_data.get("papr")),
            previous_close=StockDataMapper._safe_int(basic_data.get("bfdy_clpr")),
            close_price_change_date=basic_data.get("clpr_chng_dt")
        )

    @staticmethod
    def map_financial_position(balance_data: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]]) -> Optional[FinancialPosition]:
        """재무상태표 매핑 (balance-sheet API) - 리스트 형태로 반환"""
        if not balance_data:
            return None

        # KIS API가 리스트로 반환하므로 첫 번째 항목 사용
        if isinstance(balance_data, list):
            if not balance_data:
                return None
            balance_data = balance_data[0]

        return FinancialPosition(
            fiscal_year_month=balance_data.get("stac_yymm"),
            current_assets=StockDataMapper._safe_int(balance_data.get("cras")),
            fixed_assets=StockDataMapper._safe_int(balance_data.get("fxas")),
            total_assets=StockDataMapper._safe_int(balance_data.get("total_aset")),
            current_liabilities=StockDataMapper._safe_int(balance_data.get("flow_lblt")),
            fixed_liabilities=StockDataMapper._safe_int(balance_data.get("fix_lblt")),
            total_liabilities=StockDataMapper._safe_int(balance_data.get("cpfn")),
            capital_surplus=StockDataMapper._safe_int(balance_data.get("cfp_surp")),
            retained_earnings=StockDataMapper._safe_int(balance_data.get("prfi_surp")),
            total_equity=StockDataMapper._safe_int(balance_data.get("total_cptl"))
        )

    @staticmethod
    def map_income_statement(income_data: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]]) -> Optional[IncomeStatement]:
        """손익계산서 매핑 (income-statement API) - 리스트 형태로 반환"""
        if not income_data:
            return None

        # KIS API가 리스트로 반환하므로 첫 번째 항목 사용
        if isinstance(income_data, list):
            if not income_data:
                return None
            income_data = income_data[0]

        return IncomeStatement(
            fiscal_year_month=income_data.get("stac_yymm"),
            revenue=StockDataMapper._safe_int(income_data.get("sale_account")),
            cost_of_sales=StockDataMapper._safe_int(income_data.get("sale_cost")),
            gross_profit=StockDataMapper._safe_int(income_data.get("sale_totl_prfi")),
            net_income=StockDataMapper._safe_int(income_data.get("thtr_ntin"))
        )

    @staticmethod
    def map_financial_ratios(financial_data: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]]) -> Optional[FinancialRatios]:
        """재무비율 매핑 (financial-ratio API) - 리스트 형태로 반환"""
        if not financial_data:
            return None

        # KIS API가 리스트로 반환하므로 첫 번째 항목 사용
        if isinstance(financial_data, list):
            if not financial_data:
                return None
            financial_data = financial_data[0]

        return FinancialRatios(
            fiscal_year_month=financial_data.get("stac_yymm"),
            revenue_growth_rate=StockDataMapper._safe_decimal(financial_data.get("grs")),
            operating_profit_growth_rate=StockDataMapper._safe_decimal(financial_data.get("bsop_prfi_inrt")),
            net_income_growth_rate=StockDataMapper._safe_decimal(financial_data.get("ntin_inrt")),
            roe=StockDataMapper._safe_decimal(financial_data.get("roe_val")),
            eps=StockDataMapper._safe_decimal(financial_data.get("eps")),
            sps=StockDataMapper._safe_decimal(financial_data.get("sps")),
            bps=StockDataMapper._safe_decimal(financial_data.get("bps")),
            retention_ratio=StockDataMapper._safe_decimal(financial_data.get("rsrv_rate")),
            debt_ratio=StockDataMapper._safe_decimal(financial_data.get("lblt_rate"))
        )

    @staticmethod
    def map_profitability_ratios(profit_data: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]]) -> Optional[ProfitabilityRatios]:
        """수익성비율 매핑 (profit-ratio API) - 리스트 형태로 반환"""
        if not profit_data:
            return None

        # KIS API가 리스트로 반환하므로 첫 번째 항목 사용
        if isinstance(profit_data, list):
            if not profit_data:
                return None
            profit_data = profit_data[0]

        return ProfitabilityRatios(
            fiscal_year_month=profit_data.get("stac_yymm"),
            return_on_assets=StockDataMapper._safe_decimal(profit_data.get("cptl_ntin_rate")),
            return_on_equity=StockDataMapper._safe_decimal(profit_data.get("self_cptl_ntin_inrt")),
            net_profit_margin=StockDataMapper._safe_decimal(profit_data.get("sale_ntin_rate")),
            gross_profit_margin=StockDataMapper._safe_decimal(profit_data.get("sale_totl_rate"))
        )

    @staticmethod
    def map_stability_ratios(stability_data: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]]) -> Optional[StabilityRatios]:
        """안정성비율 매핑 (stability-ratio API) - 리스트 형태로 반환"""
        if not stability_data:
            return None

        # KIS API가 리스트로 반환하므로 첫 번째 항목 사용
        if isinstance(stability_data, list):
            if not stability_data:
                return None
            stability_data = stability_data[0]

        return StabilityRatios(
            fiscal_year_month=stability_data.get("stac_yymm"),
            debt_ratio=StockDataMapper._safe_decimal(stability_data.get("lblt_rate")),
            borrowing_dependency=StockDataMapper._safe_decimal(stability_data.get("bram_depn")),
            current_ratio=StockDataMapper._safe_decimal(stability_data.get("crnt_rate")),
            quick_ratio=StockDataMapper._safe_decimal(stability_data.get("quck_rate"))
        )

    @staticmethod
    def map_growth_ratios(growth_data: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]]) -> Optional[GrowthRatios]:
        """성장성비율 매핑 (growth-ratio API) - 리스트 형태로 반환"""
        if not growth_data:
            return None

        # KIS API가 리스트로 반환하므로 첫 번째 항목 사용
        if isinstance(growth_data, list):
            if not growth_data:
                return None
            growth_data = growth_data[0]

        return GrowthRatios(
            fiscal_year_month=growth_data.get("stac_yymm"),
            revenue_growth_rate=StockDataMapper._safe_decimal(growth_data.get("grs")),
            operating_profit_growth_rate=StockDataMapper._safe_decimal(growth_data.get("bsop_prfi_inrt")),
            equity_growth_rate=StockDataMapper._safe_decimal(growth_data.get("equt_inrt")),
            total_assets_growth_rate=StockDataMapper._safe_decimal(growth_data.get("totl_aset_inrt"))
        )

    @staticmethod
    def map_to_stock_detail_info(
        price_data: Dict[str, Any],
        basic_data: Optional[Dict[str, Any]],
        balance_data: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]],
        income_data: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]],
        financial_data: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]],
        profit_data: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]],
        stability_data: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]],
        growth_data: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]]
    ) -> StockDetailInfo:
        """전체 종목 상세 정보 매핑"""
        return StockDetailInfo(
            price=StockDataMapper.map_price_info(price_data),
            company=StockDataMapper.map_company_info(basic_data),
            financial_position=StockDataMapper.map_financial_position(balance_data),
            income_statement=StockDataMapper.map_income_statement(income_data),
            financial_ratios=StockDataMapper.map_financial_ratios(financial_data),
            profitability=StockDataMapper.map_profitability_ratios(profit_data),
            stability=StockDataMapper.map_stability_ratios(stability_data),
            growth=StockDataMapper.map_growth_ratios(growth_data)
        )

    @staticmethod
    def _safe_int(value: any) -> Optional[int]:
        """문자열을 안전하게 int로 변환"""
        if value is None or value == "":
            return None
        try:
            # 쉼표 제거 후 변환
            if isinstance(value, str):
                value = value.replace(",", "")
            return int(float(value))
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _safe_decimal(value: any) -> Optional[Decimal]:
        """문자열을 안전하게 Decimal로 변환"""
        if value is None or value == "":
            return None
        try:
            return Decimal(str(value))
        except (ValueError, TypeError):
            return None
