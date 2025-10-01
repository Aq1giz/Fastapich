from fastapi import FastAPI, Path, Depends
from fastapi import HTTPException
from database.base import books_db
from schemas import BookAddSchema, BookDeleteSchema, BookUpdateScema
import uvicorn

app = FastAPI()
books_ids = 1


@app.get("/books", tags=["Books"])
def get_books() -> dict:
    return books_db


@app.post("/books", tags=["Books"])
def add_books(book: BookAddSchema) -> dict:
    try:
        global books_ids
        book_id = books_ids + 1
        books_db[book_id] = {
            "autors": book.authors,
            "title": book.title
        }
        books_ids += 1
        return books_db
    except ValueError as e:
        error_msg = str(e[0])
        error_code = int(e[1])
        raise HTTPException(status_code=error_code, detail=error_msg)

    
@app.delete("/books", tags=["Books"])
def delete_books(book: BookDeleteSchema) -> dict:
    try:
        book_id = book.id
        del books_db[book_id]
        return books_db
    except ValueError as e:
        error_msg = str(e[0])
        error_code = int(e[1])
        HTTPException(status_code=error_code, detail=error_msg)


@app.put("/books/{book_id}", tags=["Books"])
def update_book(
        book_id: int = Path(..., gt=0),
        book: BookUpdateScema = None
    ):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="We can`t find this book. Invalid id")

    try: 
        new_book = {
            "authors": book.authors,
            "title": book.title
        }
        books_db[book_id] = new_book
        return books_db
    except ValueError as e:
        error_msg = str(e[0])
        error_code = int(e[1])
        raise HTTPException(status_code=error_code, detail=error_msg)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)