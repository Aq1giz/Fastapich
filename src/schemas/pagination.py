from pydantic import BaseModel
from pydantic import Field
from typing import Optional, Annotated


class PaginationParams(BaseModel):
    limit: Annotated[Optional[int], Field(None, ge=0, le=50, description="Кол-во элементов")]
    page: Annotated[Optional[int], Field(None, ge=0, description="Сдвиг пагинации")]