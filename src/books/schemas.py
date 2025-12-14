from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, List
from datetime import datetime, date

from src.reviews.schemas import ReviewModel


class BooksModel(BaseModel):
    uid: UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
    

class BookDetailModel(BooksModel):
    reviews: List[ReviewModel]
    

class BooksCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BooksUpdateModel(BaseModel):
    title: Optional[str] = None 
    author: Optional[str] = None
    publisher: Optional[str] = None
    published_date: Optional[date] = None
    page_count: Optional[int] = None
    language: Optional[str] = None