from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

# We use APIRouter instead of FastAPI() to make it a modular sub-component
router = APIRouter()

class Book(BaseModel):
    id: int
    title: str
    author: str
    genre: str

books_db = [
    {"id": 1, "title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy"},
    {"id": 2, "title": "1984", "author": "George Orwell", "genre": "Dystopian"}
]

@router.get("/books", response_model=List[Book])
def get_books():
    return books_db

@router.post("/books", status_code=201, response_model=Book)
def create_book(new_book: Book):
    books_db.append(new_book.model_dump())
    return new_book