from fastapi import Depends, HTTPException
from typing import Annotated
from schemas.pagination import PaginationParams

PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]