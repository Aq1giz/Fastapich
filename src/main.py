from fastapi import FastAPI, Query, HTTPException
from typing import List
import uvicorn
import asyncio

from dependensies import PaginationDep
from schemas import UsersPostScemaDTO, UsersSchemaDTO
from database import get_users_pagination_db, add_user_db, add_all_users_db, delete_user_db, create_tables

app = FastAPI()


@app.get(
    path="/users",
    description="Get all users",
    tags=["USERS"]
)
async def get_user(pagination: PaginationDep) -> List[dict]:
    try:
        users_list = await get_users_pagination_db(page=pagination.page, limit=pagination.limit)
        return [user.model_dump() for user in users_list]
    except Exception as ex_:
        raise HTTPException(
            status_code=404,
            detail=str(ex_)
        )


@app.post(
    path="/users",
    description="Add new user",
    tags=["USERS"]
)
async def add_user(user: UsersPostScemaDTO) -> List[dict]:
    try:
        result = await add_user_db(user_name=user.name)
        return [user.model_dump() for user in result]
    except Exception as ex_:
        raise HTTPException(
            status_code=404,
            detail=str(ex_)
        )


@app.delete( 
    path="/users",
    description="Delete user by ID",
    tags=["USERS"]
)
async def delete_user(user_id: int):
    try:
        result = await delete_user_db(id=user_id)
        return [user.model_dump(mode='json') for user in result]
    except ValueError as v_:
        raise HTTPException(
            status_code=404,
            detail=str(v_)
        )


async def main():
    create_tables_task = asyncio.create_task(create_tables())
    await create_tables_task
    add_all_users_task = asyncio.create_task(add_all_users_db(["Misha", "Leva", "Nekit", "Ivan", "Grisha"]))
    get_all_users_task = asyncio.create_task(get_users_pagination_db())

    await add_all_users_task
    all_users = await get_all_users_task
    print(all_users)


if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run("main:app", reload=True)