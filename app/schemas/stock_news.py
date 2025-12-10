from pydantic import BaseModel
from typing import List

class NewsItem(BaseModel):
    title: str
    original_link: str
    link: str
    description: str
    pub_date: str

class StockNewsResponse(BaseModel):
    status: int
    message: str
    data: List[NewsItem]
