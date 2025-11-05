from fastapi import status as http_status

class HTTPStatus:
    OK = http_status.HTTP_200_OK
    BAD_REQUEST = http_status.HTTP_400_BAD_REQUEST
    NOT_FOUND = http_status.HTTP_404_NOT_FOUND
    INTERNAL_ERROR = http_status.HTTP_500_INTERNAL_SERVER_ERROR

class Message:
    HEALTH_CHECK_SUCCESS = "헬스 체크에 성공했습니다."
    COMPANY_SEARCH_SUCCESS = "기업 검색에 성공했습니다."
    GET_STOCK_INFO_SUCCESS = "종목 정보 조회에 성공했습니다."
    GET_STOCK_CHART_SUCCESS = "종목 차트 조회에 성공했습니다."
    GET_EXCHANGE_RATE_SUCCESS = "환율 조회에 성공했습니다."

class ErrorMessage:
    NOT_IMPLEMENTED = "해당 기능은 아직 구현되지 않았습니다."
    DB_CONNECTION_ERROR = "데이터베이스 연결에 실패했습니다."
    EXTERNAL_API_ERROR = "외부 API 호출에 실패했습니다."
    INVALID_TICKER = "유효하지 않은 종목 코드입니다."
    COMPANY_SEARCH_NOT_FOUND = "기업 검색 결과가 없습니다."
    STOCK_NOT_FOUND = "종목 정보를 찾을 수 없습니다."
    STOCK_CHART_NOT_FOUND = "종목 차트 데이터를 찾을 수 없습니다."
    INVALID_DATE_RANGE = "유효하지 않은 날짜 범위입니다."
    INVALID_PERIOD_TYPE = "유효하지 않은 기간 구분 코드입니다."
    EXCHANGE_RATE_NOT_FOUND = "환율 정보를 찾을 수 없습니다."
    EXCHANGE_RATE_API_ERROR = "환율 API 호출에 실패했습니다."

class KISAPIConfig:
    MARKET_DIV_CODE_KRX = "J"
    MARKET_DIV_CODE_NXT = "NX"
    MARKET_DIV_CODE_UNIFIED = "UN"

    PERIOD_DIV_CODE_DAY = "D"
    PERIOD_DIV_CODE_WEEK = "W"
    PERIOD_DIV_CODE_MONTH = "M"
    PERIOD_DIV_CODE_YEAR = "Y"

    ADJUSTED_PRICE_TYPE_ADJUSTED = "0"
    ADJUSTED_PRICE_TYPE_ORIGINAL = "1"

    FID_DIV_CLS_CODE_QUARTERLY = "1"
    FID_DIV_CLS_CODE_ANNUAL = "0"

    PRODUCT_TYPE_CODE_STOCK = "300"

    TR_ID_INQUIRE_PRICE = "FHKST01010100"
    TR_ID_SEARCH_STOCK_INFO = "CTPF1002R"
    TR_ID_BALANCE_SHEET = "FHKST66430100"
    TR_ID_INCOME_STATEMENT = "FHKST66430200"
    TR_ID_FINANCIAL_RATIO = "FHKST66430300"
    TR_ID_PROFIT_RATIO = "FHKST66430400"
    TR_ID_STABILITY_RATIO = "FHKST66430600"
    TR_ID_GROWTH_RATIO = "FHKST66430800"
    TR_ID_DAILY_CHART = "FHKST03010100"

class KISAPIEndpoint:
    OAUTH_TOKEN = "/oauth2/tokenP"
    INQUIRE_PRICE = "/uapi/domestic-stock/v1/quotations/inquire-price"
    SEARCH_STOCK_INFO = "/uapi/domestic-stock/v1/quotations/search-stock-info"
    BALANCE_SHEET = "/uapi/domestic-stock/v1/finance/balance-sheet"
    INCOME_STATEMENT = "/uapi/domestic-stock/v1/finance/income-statement"
    FINANCIAL_RATIO = "/uapi/domestic-stock/v1/finance/financial-ratio"
    PROFIT_RATIO = "/uapi/domestic-stock/v1/finance/profit-ratio"
    STABILITY_RATIO = "/uapi/domestic-stock/v1/finance/stability-ratio"
    GROWTH_RATIO = "/uapi/domestic-stock/v1/finance/growth-ratio"
    DAILY_CHART = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"

class KoreaEximAPIConfig:
    DATA_TYPE_AP01 = "AP01"
    CURRENCY_CODE_USD = "USD"

class KoreaEximAPIEndpoint:
    EXCHANGE_RATE_JSON = "/site/program/financial/exchangeJSON"