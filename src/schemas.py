from pydantic import BaseModel, PydanticUserError, ValidationError
from pydantic import Field, field_validator, model_validator
from typing import Optional, Annotated
from datetime import datetime


class UsersPostScemaDTO(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=16)]
    password: Annotated[str, Field(min_length=8, max_length=64)]


class UsersSchemaDTO(UsersPostScemaDTO):
    id: int 
    created_at: datetime
    updated_at: datetime


class PaginationParams(BaseModel):
    limit: Annotated[Optional[int], Field(None, ge=0, le=50, description="Кол-во элементов")]
    page: Annotated[Optional[int], Field(None, ge=0, description="Сдвиг пагинации")]


if __name__ == "__main__":
    try: 
        user = UsersPostScemaDTO(id=1, name="ds")
    except ValidationError as e:
        print(e.errors())