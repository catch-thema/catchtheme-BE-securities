from pydantic import BaseModel
from typing import List

class KeywordItem(BaseModel):
    word: str
    count: int

class StockNewsKeywordsResponse(BaseModel):
    status: int
    message: str
    data: List[KeywordItem]
