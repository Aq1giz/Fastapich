from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import Field, field_validator
import uvicorn

app = FastAPI()


books_ids = 1
books_db = {
    1: {
        "autors": ["Mark"],
        "title": "Hello world"
    },
}

class BookAddSchema(BaseModel):
    title: str = Field(min_length=3, max_length=16, description="Title must be between 3 and 16")
    authors: list = Field(min_length=1, max_length=10, description="Count of authors must be between 1 and 10")

    @field_validator("authors")
    def lenght_author_validator(cls, value: list) -> int:
        for element in value:
            if len(element) < 3 or len(element) > 16:
                raise HTTPException(status_code=422, detail="Author name must be between 3 and 16")
        return value

class BookDeleteSchema(BaseModel):
    id: int

    @field_validator("id")
    def id_validator(cls, id: int) -> int:
        if id not in books_db.keys():
            raise HTTPException(status_code=404, detail="We can`t find this book. Invalid id")
        return id


class BookUpdateScema(BaseModel):
    id: int
    authors: list = Field(min_length=1, max_length=10, detail="Count of authors must be between 1 and 10")
    title: str = Field(min_length=3, max_length=16, detail="Title must be between 3 and 16")

    @field_validator("id")
    def id_author_validator(cls, value: str, info):
        if id not in books_db.keys():
            raise HTTPException(status_code=404, detail="We can`t find this book. Invalid id")

    @field_validator("authors")
    def id_author_validator(cls, value: list[str], info):
        for author in value:
            if len(author) < 3 or len(author) > 16:
                raise HTTPException(status_code=422, detail="Author name must be between 3 and 16")
        return value




@app.get("/books", tags=["Books"])
def get_books() -> dict:
    return books_db


@app.post("/books", tags=["Books"])
def add_books(book: BookAddSchema) -> dict:
    global books_ids
    book_id = books_ids + 1
    books_db[book_id] = {
        "autors": book.authors,
        "title": book.title
    }
    books_ids += 1
    return books_db

    
@app.delete("/books", tags=["Books"])
def delete_books(book: BookDeleteSchema) -> dict:
    book_id = book.id
    del books_db[book_id]
    return books_db


@app.put("/books", tags=["Books"])
def update_book(book: BookUpdateScema):
    book_id = book.id
    new_book = {
        "authors": book.authors,
        "title": book.title
    }
    books_db[book_id] = new_book
    return books_db


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)