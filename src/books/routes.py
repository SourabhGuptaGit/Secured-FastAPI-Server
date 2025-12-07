from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from uuid import UUID

from src.books.books_data import books
from src.books.services import BookService
from src.books.schemas import BooksCreateModel, BooksModel, BooksUpdateModel
from src.db.db_agent import get_session


book_route = APIRouter()

def get_book_service():
    return BookService()

@book_route.get("/", response_model=List[BooksModel])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    book_service: BookService = Depends(get_book_service)
):
    data = await book_service.get_all_books(session=session)
    return data


@book_route.get("/{id}", response_model=BooksModel, status_code=status.HTTP_200_OK)
async def get_book(
    book_id: UUID,
    session: AsyncSession = Depends(get_session),
    book_service: BookService = Depends(get_book_service)
):
    book_data = await book_service.get_book(book_id, session=session)
    
    if book_data:
        return book_data
    else:
        raise HTTPException(status_code=404, detail=f"Invalid ID - {id}")


@book_route.post("/", response_model=BooksModel, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BooksCreateModel,
    session: AsyncSession = Depends(get_session),
    book_service: BookService = Depends(get_book_service)
):
    new_book_data = await book_service.create_book(book_data=book_data, session=session)
    if new_book_data:
        return new_book_data
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid data format.")


@book_route.patch("/{id}", response_model=BooksModel, status_code=status.HTTP_200_OK)
async def update_book(
    book_id: UUID,
    book_data: BooksUpdateModel,
    session: AsyncSession = Depends(get_session),
    book_service: BookService = Depends(get_book_service)
):
    updated_book_data = await book_service.update_book(
        book_id=book_id, book_data=book_data, session=session
        )
    if updated_book_data:
        return updated_book_data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid ID - {book_id}")
    

@book_route.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: UUID,
    session: AsyncSession = Depends(get_session),
    book_service: BookService = Depends(get_book_service)
):
    deleted_book_data = await book_service.delete_book(book_id=book_id, session=session)
    if not deleted_book_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid ID - {book_id}")

        

# @book_route.get("/", response_model=List[BooksModel])
# async def get_all_books(session: AsyncSession = Depends(get_session)):
#     data = [BooksModel(**book) for book in books]
#     return data


# @book_route.get("/{id}")
# async def get_book(id: int, session: AsyncSession = Depends(get_session)):
#     for book in books:
#         book_obj = BooksModel(**book)
#         if book_obj.id == id:
#             return book_obj
#     return HTTPException(status_code=404, detail=f"Invalid ID - {id}")


# @book_route.post("/", status_code=status.HTTP_201_CREATED)
# async def create_book(book: BooksModel, session: AsyncSession = Depends(get_session)):
#     books.append(book.model_dump())
#     return {"message": book}


# @book_route.patch("/{id}", status_code=status.HTTP_200_OK)
# async def update_book(id: int, new_book: BooksUpdateModel, session: AsyncSession = Depends(get_session)):
#     new_book_raw = None
#     for book in books:
#         book_obj = BooksModel(**book)
#         if book_obj.id == id:
#             new_book_raw = new_book.model_dump()
#             new_book_raw["id"] = id
#             new_book_raw["published_date"] = book_obj.published_date
#             new_book_raw = BooksModel(**new_book_raw)
#             books.remove(book)
#             books.append(new_book_raw.model_dump())
#             break
    
#     if not new_book_raw:
#         return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid ID - {id}")
    
#     return new_book_raw
    

# @book_route.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_book(id: int, session: AsyncSession = Depends(get_session)):
#     for book in books.copy():
#         book_obj = BooksModel(**book)
#         if book_obj.id == id:
#             books.remove(book)
#             return {}
    
#     return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid ID - {id}")
        
        