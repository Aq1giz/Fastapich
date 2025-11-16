from fastapi import APIRouter, HTTPException, status
from typing import List

from .. import PaginationDep
from .. import UsersPostScemaDTO
from .. import UsersSchemaDTO
from ..database import get_users_pagination_db
from ..database import add_user_db
from ..database import delete_user_db
from ..database import update_user_db


router = APIRouter(
    tags=["CRUD"],
)

@router.get(
    description="Get all users",
    path="/crud-users"
)
async def get_user(pagination: PaginationDep) -> List[dict]:
    try:
        users_list = await get_users_pagination_db(page=pagination.page, limit=pagination.limit)
        return [user.model_dump() for user in users_list]
    except ValueError as v_:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(v_)
        )


@router.post(
    description="Add new user",
    path="/crud-users"
)
async def add_user(user: UsersPostScemaDTO) -> List[dict]:
    try:
        result = await add_user_db(
            username=user.username,
            password=user.password
        )
        return [user.model_dump() for user in result]
    except ValueError as v_:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(v_)
        )


@router.delete(
    description="Delete user by ID",
    path="/crud-users"
)
async def delete_user(user_id: int):
    try:
        result = await delete_user_db(id=user_id)
        return [user.model_dump(mode='json') for user in result]
    except ValueError as v_:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(v_)
        )
    

@router.put(
    description="Update user by ID",
    path="/crud-users"
)
async def update_user(
    user: UsersPostScemaDTO,
    user_id: int
) -> List[UsersSchemaDTO]:
    try:
        result = await update_user_db(
            user_id=user_id,
            new_username=user.username
        )
        return result
    except ValueError as v_:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(v_)
        )