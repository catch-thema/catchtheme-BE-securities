from sqlalchemy import Column, String, Integer
from app.db.base import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    company_name = Column(String(255), nullable=False, index=True)
    ticker = Column(String(20), unique=True, nullable=False, index=True)

    def __repr__(self):
        return f"<Company(id={self.id}, name={self.company_name}, ticker={self.ticker})>"
    