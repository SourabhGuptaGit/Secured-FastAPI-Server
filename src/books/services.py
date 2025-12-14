from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc

from src.books.schemas import BooksCreateModel, BooksUpdateModel
from src.db.models import Books


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Books).order_by(desc(Books.created_at))
        result = await session.exec(statement)
        books_data = result.all()
        return books_data if books_data else []
    
    async def get_all_books_for_user(self, user_uid, session: AsyncSession):
        statement = select(Books).where(Books.user_uid == user_uid).order_by(desc(Books.created_at))
        result = await session.exec(statement)
        books_data = result.all()
        return books_data if books_data else []
    
    async def get_book(self, book_id: str, session: AsyncSession):
        statement = select(Books).where(Books.uid == book_id)
        result = await session.exec(statement)
        book_data = result.first()
        return book_data if book_data else None
    
    async def create_book(self, book_data: BooksCreateModel, user_uid, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book_data = Books(**book_data_dict)
        new_book_data.user_uid = user_uid
        try:
            new_book_data.published_date = datetime.strptime(book_data_dict.get("published_date"), "%Y-%m-%d").date()
        except ValueError:
            return None
        session.add(new_book_data)
        await session.commit()
        return new_book_data
    
    async def update_book(self, book_id: str, book_data: BooksUpdateModel, session: AsyncSession):
        existing_book_data = await self.get_book(book_id, session)
        if not existing_book_data:
            return None
        
        new_book_data = book_data.model_dump(exclude_none=True)
        if not new_book_data:
            return None
        
        for k, v in new_book_data.items():
            setattr(existing_book_data, k, v)
        
        await session.commit()
        return existing_book_data
    
    async def delete_book(self, book_id: str, session: AsyncSession):
        existing_book_data = await self.get_book(book_id, session)
        if not existing_book_data:
            return None
        
        await session.delete(existing_book_data)
        await session.commit()
        return existing_book_data