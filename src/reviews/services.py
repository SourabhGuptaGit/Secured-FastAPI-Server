from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status

from src.reviews.schemas import ReviewModel
from src.db.models import Reviews, User, Books
from src.auth.services import UserService
from src.books.services import BookService


user_service = UserService()
book_service = BookService()

class ReviewService:
    
    async def get_reviews_for_book(self, book_uid: str, session: AsyncSession):
        statement = select(Reviews).where(Reviews.book_uid == book_uid).order_by(desc(Reviews.rating))
        reviews = await session.exec(statement)
        return reviews
    
    async def add_reviews_for_book(self, user_email: str, book_uid: str, review_data: ReviewModel, session: AsyncSession):
        
        user = await user_service.get_user_by_email(email=user_email, session=session)
        book = await book_service.get_book(book_id=book_uid, session=session)
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")
        
        new_review_data = Reviews(**review_data.model_dump())
        new_review_data.book = book
        new_review_data.user = user
        session.add(new_review_data)
        await session.commit()
        return new_review_data