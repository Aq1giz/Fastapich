from fastapi import Query, HTTPException, status
from typing import List
import uvicorn
import asyncio

from main import app

@app.get(
    path="/crud-users",
    description="Get all users",
    tags=["USERS"]
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


@app.post(
    path="/crud-users",
    description="Add new user",
    tags=["USERS"]
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


@app.delete( 
    path="/crud-users",
    description="Delete user by ID",
    tags=["USERS"]
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
    

@app.put(
    path="/crud-users",
    description="Update user by ID",
    tags=["USERS"]
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