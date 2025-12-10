from app.db.base import Base
from app.db.session import engine
from app.models.company import Company, StockInfo

def create_tables():
    print("🔄 테이블 생성 중...")
    Base.metadata.create_all(bind=engine)
    print("✅ 테이블이 생성되었습니다.")


def drop_tables():
    print("🔄 테이블 삭제 중...")
    Base.metadata.drop_all(bind=engine)
    print("✅ 테이블이 삭제되었습니다.")


if __name__ == "__main__":
    create_tables()