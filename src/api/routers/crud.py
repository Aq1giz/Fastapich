from fastapi import APIRouter, HTTPException, status
from typing import List

from .. import PaginationDep
from .. import UsersPostSchema
from .. import UsersSchemaDTO
from ..database import get_users_pagination_db
from ..database import add_user_db
from ..database import delete_user_db
from ..database import update_user_db
from ..utils import get_hashed_password_and_salt


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
async def add_user(user: UsersPostSchema) -> List[dict]:
    try:
        hashed_password, salt = get_hashed_password_and_salt(user.password)
        result = await add_user_db(
            username=user.username,
            password=hashed_password,
            salt=salt,
        )
        return [user.model_dump(mode='json') for user in result]
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
    user: UsersPostSchema,
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