from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from uuid import UUID

from src.books.books_data import books
from src.books.services import BookService
from src.books.schemas import BooksCreateModel, BooksModel, BooksUpdateModel, BookDetailModel
from src.db.db_agent import get_session
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.db.models import ROLES


book_route = APIRouter()
role_checker = Depends(
    RoleChecker([ROLES.USER.value, ROLES.ADMIN.value])
)

def get_book_service():
    return BookService()


access_token_bearer = AccessTokenBearer()


@book_route.get("/", response_model=List[BooksModel], dependencies=[role_checker])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    book_service: BookService = Depends(get_book_service),
    access_user_details: dict = Depends(access_token_bearer)
):
    data = await book_service.get_all_books(session=session)
    return data


@book_route.get("/user/{user_uid}", response_model=List[BooksModel], dependencies=[role_checker])
async def get_books_for_user(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    book_service: BookService = Depends(get_book_service),
    access_user_details: dict = Depends(access_token_bearer)
):
    data = await book_service.get_all_books_for_user(user_uid=user_uid, session=session)
    return data


@book_route.get("/{book_id}", response_model=BookDetailModel, dependencies=[role_checker])
async def get_book(
    book_id: UUID,
    session: AsyncSession = Depends(get_session),
    book_service: BookService = Depends(get_book_service),
    access_user_details: dict = Depends(access_token_bearer)
):
    book_data = await book_service.get_book(book_id, session=session)
    if not book_data:
        raise HTTPException(status_code=404, detail=f"Invalid ID - {id}")
    
    return book_data


@book_route.post("/", response_model=BooksModel, status_code=status.HTTP_201_CREATED, dependencies=[role_checker])
async def create_book(
    book_data: BooksCreateModel,
    session: AsyncSession = Depends(get_session),
    book_service: BookService = Depends(get_book_service),
    access_user_details: dict = Depends(access_token_bearer)
    ):
    
    user_uid = access_user_details.get("user").get("user_uid")
    new_book_data = await book_service.create_book(book_data=book_data, user_uid=user_uid, session=session)
    if new_book_data:
        return new_book_data
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid data format.")


@book_route.patch("/{id}", response_model=BooksModel, status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def update_book(
    book_id: UUID,
    book_data: BooksUpdateModel,
    session: AsyncSession = Depends(get_session),
    book_service: BookService = Depends(get_book_service),
    access_user_details: dict = Depends(access_token_bearer)
):
    updated_book_data = await book_service.update_book(
        book_id=book_id, book_data=book_data, session=session
        )
    if updated_book_data:
        return updated_book_data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid ID - {book_id}")
    

@book_route.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(
    book_id: UUID,
    session: AsyncSession = Depends(get_session),
    book_service: BookService = Depends(get_book_service),
    access_user_details: dict = Depends(access_token_bearer)
):
    deleted_book_data = await book_service.delete_book(book_id=book_id, session=session)
    if not deleted_book_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid ID - {book_id}")
