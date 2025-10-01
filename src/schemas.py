from pydantic import BaseModel
from pydantic import Field, field_validator, model_validator
from database.base import books_db


class BookAddSchema(BaseModel):
    title: str = Field(min_length=3, max_length=16, description="Title must be between 3 and 16")
    authors: list = Field(min_length=1, max_length=10, description="Count of authors must be between 1 and 10")

    @field_validator("authors")
    def lenght_author_validator(cls, value: list) -> int:
        for element in value:
            if len(element) < 3 or len(element) > 16:
                raise ValueError("Author name must be between 3 and 16", 422)
        return value

class BookDeleteSchema(BaseModel):
    id: int

    @field_validator("id")
    def id_validator(cls, id: int) -> int:
        if id not in books_db.keys():
            raise ValueError("We can`t find this book. Invalid id", 404)
        return id


class BookUpdateScema(BaseModel):
    authors: list
    title: str = Field(min_length=3, max_length=16, detail="Title must be between 3 and 16")

    @field_validator("authors")
    def id_author_validator(cls, value: list[str]):
        if len(value) < 1 or len(value) > 10:
            raise ValueError("Count of authors must be between 1 and 10", 422)
        for author in value:
            if len(author) < 3 or len(author) > 16:
                raise ValueError("Author name must be between 3 and 16", 422)
        return value