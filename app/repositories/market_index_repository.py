from typing import Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.models.market_index import MarketIndex
from app.schemas.index import IndexData


class MarketIndexRepository:

    def __init__(self, db: Session):
        self.db = db

    def upsert_index(self, index_data: IndexData) -> MarketIndex:
        stmt = insert(MarketIndex).values(
            code=index_data.code,
            name=index_data.name,
            current_price=index_data.current_price,
            change_rate=index_data.change_rate,
            change_price=index_data.change_price,
            timestamp=index_data.timestamp
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=['code'],
            set_={
                'current_price': index_data.current_price,
                'change_rate': index_data.change_rate,
                'change_price': index_data.change_price,
                'timestamp': index_data.timestamp
            }
        )

        self.db.execute(stmt)
        self.db.commit()

        return self.db.query(MarketIndex).filter(MarketIndex.code == index_data.code).first()

    def get_index_by_code(self, code: str) -> Optional[MarketIndex]:
        return self.db.query(MarketIndex).filter(MarketIndex.code == code).first()

    def get_all_indices(self) -> Dict[str, MarketIndex]:
        indices = self.db.query(MarketIndex).all()
        return {index.code: index for index in indices}
