from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    uid: UUID = Field(sa_column=Column(
        pg.UUID,
        primary_key=True,
        default=uuid4
    ))
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP , default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP , default=datetime.now))
    
    def __repr__(self):
        return f"<User: Name - {self.username}>"