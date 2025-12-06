from typing import List
from fastapi import APIRouter, HTTPException, status

from src.books.books_data import books
from src.books.schemas import BooksModel, BooksUpdateModel


book_route = APIRouter()

@book_route.get("/", response_model=List[BooksModel])
async def get_all_books():
    data = [BooksModel(**book) for book in books]
    return data


@book_route.get("/{id}")
async def get_book(id: int):
    for book in books:
        book_obj = BooksModel(**book)
        if book_obj.id == id:
            return book_obj
    return HTTPException(status_code=404, detail=f"Invalid ID - {id}")


@book_route.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: BooksModel):
    books.append(book.model_dump())
    return {"message": book}


@book_route.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_book(id: int, new_book: BooksUpdateModel):
    new_book_raw = None
    for book in books:
        book_obj = BooksModel(**book)
        if book_obj.id == id:
            new_book_raw = new_book.model_dump()
            new_book_raw["id"] = id
            new_book_raw["published_date"] = book_obj.published_date
            new_book_raw = BooksModel(**new_book_raw)
            books.remove(book)
            books.append(new_book_raw.model_dump())
            break
    
    if not new_book_raw:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid ID - {id}")
    
    return new_book_raw
    

@book_route.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int):
    for book in books.copy():
        book_obj = BooksModel(**book)
        if book_obj.id == id:
            books.remove(book)
            return {}
    
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid ID - {id}")
        
        