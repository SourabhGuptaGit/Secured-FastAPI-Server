from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.db_agent import get_session
from src.auth.dependencies import get_current_auth_user, AccessTokenBearer
from src.reviews.schemas import ReviewCreateModel
from src.reviews.services import ReviewService
from src.db.models import User


review_router = APIRouter()

review_services = ReviewService()
access_token_bearer = AccessTokenBearer()


@review_router.post("/book/{book_uid}")
async def add_review_to_book(
    book_uid: str,
    review_data: ReviewCreateModel,
    user_details: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(get_session)
    ):
    
    print("\n\n\n\n\n")
    print("Hi")
    new_review_details = await review_services.add_reviews_for_book(
        user_email=user_details.email, book_uid=book_uid, review_data=review_data, session=session
    )
    return new_review_details
    