class Status:
    OK = "ok"
    ERROR = "error"

class Message:
    HEALTH_CHECK_SUCCESS = "헬스 체크에 성공했습니다."
    COMPANY_SEARCH_SUCCESS = "기업 검색에 성공했습니다."
    COMPANY_SEARCH_NOT_FOUND = "기업 검색 결과가 없습니다."

class ErrorMessage:
    NOT_IMPLEMENTED = "해당 기능은 아직 구현되지 않았습니다."
    DB_CONNECTION_ERROR = "데이터베이스 연결에 실패했습니다."