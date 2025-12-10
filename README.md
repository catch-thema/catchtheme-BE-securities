# UPssue 백엔드 증권 서버

UPssue 백엔드 증권 서버 (Python / FastAPI)

한국 증권 시장의 주식, 환율, 뉴스 정보를 제공하는 REST API 백엔드 서비스

## 주요 기능

### 1. 종목 정보 조회
- **종목 상세 정보**: 실시간 가격, 기업 정보, 재무제표 조회
- **기간별 시세**: 일/주/월/연봉 차트 데이터 제공
- **전종목 조회**: KRX 전체 상장 종목 리스트 (페이지네이션 지원)
- **기업 검색**: 종목명 기반 검색 기능

### 2. 뉴스 분석
- **종목 관련 뉴스 조회**: 네이버 뉴스 API를 통한 종목별 뉴스 수집
- **키워드 추출**: KoNLPy 기반 뉴스 텍스트 분석 및 주요 키워드 추출

### 3. 환율 정보
- **USD/KRW 환율 조회**: 한국수출입은행 API를 통한 실시간 환율 정보
- **자동 업데이트**: 3분마다 환율 자동 갱신 (APScheduler)

## 기술 스택

| Type | Skills |
| :---: | --- |
| 백엔드 프레임워크 | FastAPI, Uvicorn, Pydantic |
| 데이터베이스 | PostgreSQL, SQLAlchemy, Alembic |
| 외부 API 연동 | 한국투자증권(KIS) API, 한국거래소(KRX) API, 한국수출입은행 API, 네이버 검색 API |
| 기타 | KoNLPy, APScheduler |

## 프로젝트 구조

```
catchtheme-BE-securities/
├── app/
│   ├── api/                          # API 엔드포인트
│   │   ├── endpoints/
│   │   │   ├── health.py            # 헬스 체크
│   │   │   ├── search.py            # 기업 검색
│   │   │   ├── stock_info.py        # 종목 정보 조회
│   │   │   ├── exchange_rate.py     # 환율 조회
│   │   │   └── stock_news.py        # 뉴스 조회 및 키워드 추출
│   │   └── router.py                # API 라우터 통합
│   ├── core/                         # 핵심 설정
│   │   ├── config.py                # 환경 설정
│   │   └── constants.py             # 상수
│   ├── models/                       # SQLAlchemy ORM 모델
│   ├── schemas/                      # Pydantic 스키마
│   ├── repositories/                 # 데이터 액세스 계층
│   ├── services/                     # 비즈니스 로직
│   ├── utils/                        # 유틸리티
│   │   ├── kis_client.py            # KIS API 클라이언트
│   │   ├── krx_client.py            # KRX API 클라이언트
│   │   ├── koreaexim_client.py      # 환율 API 클라이언트
│   │   ├── naver_client.py          # 네이버 API 클라이언트
│   │   └── keyword_extractor.py     # 키워드 추출기
│   ├── scheduler/                    # 백그라운드 스케줄러
│   ├── db/                           # 데이터베이스 설정
│   └── main.py                       # FastAPI 앱 진입점
├── alembic/                          # DB 마이그레이션
├── requirements.txt
└── .env.example
```

## API 엔드포인트

### 종목 정보
- `GET /api/securities/search` - 기업 검색
- `GET /api/securities/stocks/{ticker}` - 종목 상세 정보
- `GET /api/securities/stocks/{ticker}/chart` - 기간별 시세 조회
- `GET /api/securities/stocks` - 전종목 정보 조회

### 뉴스 분석
- `GET /api/securities/stock-news` - 종목 관련 뉴스 조회
- `GET /api/securities/stock-news/keywords` - 뉴스 기반 키워드 추출

### 환율
- `GET /api/securities/exchange-rates/usd` - USD/KRW 환율 조회

### 시스템
- `GET /api/health` - 헬스 체크

## 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/catch-thema/catchtheme-BE-securities.git
cd catchtheme-BE-securities
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
`.env.example` 파일을 `.env`로 복사하고 필요한 값을 설정합니다.

```bash
cp .env.example .env
```

### 5. 데이터베이스 마이그레이션
```bash
alembic upgrade head
```

### 6. 서버 실행
```bash
uvicorn app.main:app --reload
```

서버는 기본적으로 [http://localhost:8000](http://localhost:8000)에서 실행됩니다.

## API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## 주요 기능 상세

### 종목 상세 정보 조회
한국투자증권 API를 통해 다음 정보를 제공합니다:
- 실시간 가격 정보 (현재가, 시가, 고가, 저가, 거래량 등)
- 기업 기본 정보 (결산월, 상장주수, 자본금 등)
- 재무상태표 (자산, 부채, 자본)
- 손익계산서 (매출, 비용, 이익)
- 재무비율 (ROE, EPS, BPS 등)
- 수익성, 안정성, 성장성 비율

### 뉴스 기반 키워드 추출
1. 네이버 뉴스 API로 종목 관련 뉴스 수집
2. KoNLPy의 OKT 형태소 분석기로 명사 추출
3. 한글 불용어 필터링
4. 빈도 기반 상위 키워드 추출

### 환율 자동 업데이트
- APScheduler를 사용하여 3분마다 자동 업데이트
- 이전 환율과 비교하여 변화율 계산
- PostgreSQL에 저장 및 캐싱
