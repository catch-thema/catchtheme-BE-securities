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

    TR_ID_DAILY_CHART = "FHKST03010100"