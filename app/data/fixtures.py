
MOCK_COMPANIES = [
    {"company_name": "삼성전자", "ticker": "005930"},
    {"company_name": "삼성전기", "ticker": "005931"},
    {"company_name": "삼성SDS", "ticker": "005932"},
    {"company_name": "삼성DX", "ticker": "005933"},
    {"company_name": "삼성카드", "ticker": "005934"},
    {"company_name": "삼성생명", "ticker": "005935"},
    {"company_name": "SK하이닉스", "ticker": "006600"},
    {"company_name": "NAVER", "ticker": "035420"},
    {"company_name": "카카오", "ticker": "035720"},
    {"company_name": "현대차", "ticker": "005380"},
    {"company_name": "LG에너지솔루션", "ticker": "373220"},
    {"company_name": "삼성바이오로직스", "ticker": "207940"},
    {"company_name": "기아", "ticker": "002700"},
    {"company_name": "셀트리온", "ticker": "068270"},
    {"company_name": "POSCO홀딩스", "ticker": "005490"},
    {"company_name": "LG화학", "ticker": "051910"},
    {"company_name": "삼성SDI", "ticker": "006400"},
    {"company_name": "현대모비스", "ticker": "012330"},
    {"company_name": "KB금융", "ticker": "105560"},
    {"company_name": "신한지주", "ticker": "055550"},
]

def generate_mock_companies(count: int = 500) -> list[dict]:

    companies = MOCK_COMPANIES.copy()

    for i in range(len(MOCK_COMPANIES), count):
        companies.append({
            "company_name": f"테스트기업{i:03d}",
            "ticker": f"{i:06d}"
        })
    
    return companies[:count]
    