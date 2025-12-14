# from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime, date
from enum import StrEnum, auto
from typing import List, Optional
import uuid


class ROLES(StrEnum):
    USER = auto()
    ADMIN = auto()


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    uid: UUID = Field(
        sa_column=Column( pg.UUID, primary_key=True, default=uuid4 )
    )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(
        sa_column=Column( pg.VARCHAR, nullable=False, server_default=ROLES.USER.value )
    )
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP , default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP , default=datetime.now))
    books: List["Books"] = Relationship( # type: ignore
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    reviews: List["Reviews"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    
    def __repr__(self):
        return f"<User: Name - {self.username}>"


class Books(SQLModel, table=True):
    __tablename__ = "books"
    uid: uuid.UUID = Field(
        sa_column=Column( pg.UUID, primary_key=True, unique=True, default=uuid.uuid4 )
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now))
    user: Optional[User] = Relationship(back_populates="books")
    reviews: List["Reviews"] = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<Book: ID - {self.uid} Title - {self.title}>"


class Reviews(SQLModel, table=True):
    __tablename__ = "reviews"
    uid: uuid.UUID = Field(
        sa_column=Column( pg.UUID, primary_key=True, unique=True, default=uuid.uuid4 )
    )
    rating: int = Field(le=5, ge=0)
    review_text: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now))
    user: Optional[User] = Relationship(back_populates="reviews")
    book: Optional[Books] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review: book - {self.book_uid} by User - {self.user_uid}>"