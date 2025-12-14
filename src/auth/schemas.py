from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List

from src.books.schemas import BooksModel
from src.reviews.schemas import ReviewModel


class UserCreateModel(BaseModel):
    username: str = Field(max_length=40)
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    email: str = Field(max_length=60)
    password: str = Field(max_length=6)
    

class UserModel(BaseModel):
    uid: UUID
    username: str = Field(max_length=40)
    email: str = Field(max_length=60)
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime
    # books: List[BooksModel] before it was here now shifted to new class.

    model_config = ConfigDict(from_attributes=True)


class UserBooksModel(UserModel):
    books: List[BooksModel]
    reviews: List[ReviewModel]


class UserLoginModel(BaseModel):
    email: str
    password: str


# class TokenUserPayload(BaseModel):
#     email: str
#     user_uid: UUID
    
# class JWTPayload(BaseModel):
#     exp: datetime
#     jti: str
#     user: TokenUserPayload
#     refresh: bool = False