from pydantic import BaseModel, ConfigDict, Field

from uuid import UUID
from datetime import datetime



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
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)