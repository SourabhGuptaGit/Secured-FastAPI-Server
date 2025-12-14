from pydantic import BaseModel, ConfigDict, Field
import uuid
from datetime import datetime
from typing import Optional



class ReviewModel(BaseModel):
    uid: uuid.UUID
    rating: int = Field(le=5, ge=0)
    review_text: str
    user_uid: Optional[uuid.UUID]
    book_uid: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime
    

class ReviewCreateModel(BaseModel):
    rating: int = Field(le=5, ge=0)
    review_text: str
    