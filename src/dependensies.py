from fastapi import Depends, HTTPException
from typing import Annotated
from schemas import PaginationParams

PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]