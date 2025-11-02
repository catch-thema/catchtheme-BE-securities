import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.init_db import create_tables
from app.models.company import Company, StockInfo
from app.data.fixtures import generate_mock_companies, generate_mock_stock_info


def seed_companies(db: Session, count: int = 500):
    existing_count = db.query(Company).count()
    
    if existing_count > 0:
        print(f"⚠️  이미 {existing_count}개의 기업 데이터가 존재합니다.")
        response = input("기존 데이터를 삭제하고 다시 생성하시겠습니까? (y/N): ")
        
        if response.lower() != 'y':
            print("초기화를 취소합니다.")
            return
        
        db.query(StockInfo).delete()
        db.query(Company).delete()
        db.commit()
        print("✅ 기존 데이터가 삭제되었습니다.")
    
    print(f"🔄 {count}개의 기업 데이터를 생성 중...")
    
    companies_data = generate_mock_companies(count)
    companies = [
        Company(
            company_name=data["company_name"],
            ticker=data["ticker"]
        )
        for data in companies_data
    ]
    
    db.bulk_save_objects(companies)
    db.commit()
    
    print(f"✅ {count}개의 기업 데이터가 성공적으로 생성되었습니다.")

def seed_stock_info(db: Session):
    companies = db.query(Company).all()

    if not companies:
        print("❌ 기업 데이터가 없습니다. 먼저 기업 데이터를 생성해주세요.")
        return
    
    print(f"🔄 {len(companies)}개의 주가 정보를 생성 중...")
    
    stock_infos = []
    for company in companies:
        stock_data = generate_mock_stock_info(company.ticker)
        
        stock_info = StockInfo(
            company_id=company.id,
            ticker=company.ticker,
            current_price=stock_data["current_price"],
            opening_price=stock_data["opening_price"],
            high_price=stock_data["high_price"],
            low_price=stock_data["low_price"],
            volume=stock_data["volume"],
            transaction_amount=stock_data["transaction_amount"],
            market_cap=stock_data["market_cap"],
            per=stock_data["per"],
            pbr=stock_data["pbr"],
            roe=stock_data["roe"],
            psr=stock_data["psr"],
            dividend_yield=stock_data["dividend_yield"],
        )
        stock_infos.append(stock_info)
    
    db.bulk_save_objects(stock_infos)
    db.commit()
    
    print(f"✅ {len(stock_infos)}개의 주가 정보가 성공적으로 생성되었습니다.")

def main():
    print("=" * 60)
    print("📊 증권 도메인 초기 데이터 생성")
    print("=" * 60)
    
    create_tables()
    
    db = SessionLocal()
    try:
        seed_companies(db, 500)
        print()
        seed_stock_info(db)
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()
    
    print()
    print("=" * 60)
    print("✅ 초기화 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()