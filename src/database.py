from sqlalchemy.orm import InspectionAttrExtensionType
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, ScalarResult
from functools import wraps
from base import session_fabric, engine
from models import Base, UsersORM
from schemas import UsersSchemaDTO
from typing import List, Optional

import asyncio
import random
import time

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


def get_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with session_fabric() as session:
            try:
                result = await func(*args, session=session, **kwargs)
                return result
            except ValueError as v_:
                await session.rollback()
                raise ValueError(v_)
    return wrapper


async def get_all_users_dto(
    session: AsyncSession,
    limit: Optional[int] = None,
    page: Optional[int] = None
) -> List[UsersSchemaDTO]:
    limit = None if page is None else limit
    offset = None if page is None or limit is None else (page) * limit
    query = (
        select(UsersORM)
        .limit(limit)
        .offset(offset)
    )
    result = await session.scalars(query)
    result_dto = [UsersSchemaDTO.model_validate(row, from_attributes=True) for row in result]
    return result_dto


@get_session
async def get_user_id():
    pass


@get_session
async def get_users_pagination_db(
    session: AsyncSession = None,
    limit: Optional[int] = None,
    page: Optional[int] = None
) -> List[UsersSchemaDTO]:
    result =  await get_all_users_dto(session, limit=limit, page=page)
    return result

@get_session
async def add_user_db(
    user_name: str,
    session: AsyncSession = None
) -> List[UsersSchemaDTO]:
    user = UsersORM(name=user_name)
    session.add(user)
    await session.commit()
    return await get_all_users_dto(session)


@get_session
async def add_all_users_db(
    user_names: List[str],
    session: AsyncSession = None
) -> List[UsersSchemaDTO]:
    
    users_list = [UsersORM(name=user_name) for user_name in user_names]
    session.add_all(users_list)
    await session.commit()
    result = await get_all_users_dto(session)
    return result


@get_session
async def delete_user_db(
    id: int,
    session: AsyncSession = None
) -> List[UsersSchemaDTO]:
    
    user = await session.get(UsersORM, id)
    if user:
        await session.delete(user)
        await session.commit()
        result = await get_all_users_dto(session)
        return result
    else:
        raise ValueError("There is no such ID")


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