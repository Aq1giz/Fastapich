# В src/api/dependencies.py
from fastapi import Depends, HTTPException
from typing import Annotated

# Импорт напрямую из schemas
from schemas.pagination import PaginationParams

PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]