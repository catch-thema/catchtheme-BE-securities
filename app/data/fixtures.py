from decimal import Decimal
import random

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

MOCK_STOCK_INFO = {
    "005930": {
        "current_price": 72000,
        "opening_price": 71500,
        "high_price": 72500,
        "low_price": 71000,
        "volume": 15234567,
        "transaction_amount": 1095690824000,
        "market_cap": 430000000000000,
        "per": Decimal("12.5"),
        "pbr": Decimal("1.2"),
        "roe": Decimal("9.6"),
        "psr": Decimal("1.5"),
        "dividend_yield": Decimal("2.8"),
    },
    "006600": {
        "current_price": 130000,
        "opening_price": 128000,
        "high_price": 131000,
        "low_price": 127500,
        "volume": 2345678,
        "transaction_amount": 304938140000,
        "market_cap": 9460000000000000,
        "per": Decimal("8.3"),
        "pbr": Decimal("1.1"),
        "roe": Decimal("12.3"),
        "psr": Decimal("1.8"),
        "dividend_yield": Decimal("1.5"),
    },
}

def generate_mock_companies(count: int = 500) -> list[dict]:

    companies = MOCK_COMPANIES.copy()

    for i in range(len(MOCK_COMPANIES), count):
        companies.append({
            "company_name": f"테스트기업{i:03d}",
            "ticker": f"{i:06d}"
        })
    
    return companies[:count]
    
def get_mock_stock_info(ticker: str) -> dict:
    
    return MOCK_STOCK_INFO.get(ticker, {
        "current_price": 50000,
        "opening_price": 49500,
        "high_price": 50500,
        "low_price": 49000,
        "volume": 1000000,
        "transaction_amount": 50000000000,
        "market_cap": 10000000000000,
        "per": Decimal("15.0"),
        "pbr": Decimal("1.5"),
        "roe": Decimal("10.0"),
        "psr": Decimal("2.0"),
        "dividend_yield": Decimal("2.0"),
    })

def generate_mock_stock_info(ticker: str, base_price: int = None) -> dict:

    if ticker in MOCK_STOCK_INFO:
        return MOCK_STOCK_INFO[ticker]
    
    if base_price is None:
        base_price = random.randint(10000, 200000)
    
    opening_price = int(base_price * random.uniform(0.97, 1.03))
    high_price = int(max(base_price, opening_price) * random.uniform(1.00, 1.05))
    low_price = int(min(base_price, opening_price) * random.uniform(0.95, 1.00))

    volume = random.randint(100000, 10000000)
    transaction_amount = base_price * volume
    market_cap = base_price * random.randint(1000000, 100000000)

    return {
        "current_price": base_price,
        "opening_price": opening_price,
        "high_price": high_price,
        "low_price": low_price,
        "volume": volume,
        "transaction_amount": transaction_amount,
        "market_cap": market_cap,
        "per": Decimal(str(round(random.uniform(5.0, 30.0), 2))),
        "pbr": Decimal(str(round(random.uniform(0.5, 5.0), 2))),
        "roe": Decimal(str(round(random.uniform(3.0, 20.0), 2))),
        "psr": Decimal(str(round(random.uniform(0.5, 5.0), 2))),
        "dividend_yield": Decimal(str(round(random.uniform(0.0, 5.0), 2))),
    }
