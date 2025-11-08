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
    """ Удаление и создание таблиц. """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


""" Декоратор для получения сессий. """
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
    """
    SELECT * FROM users
    LIMIT limit OFFSET offset;
    """
    limit = None if page is None else limit
    offset = None if page is None or limit is None else (page) * limit
    query = (
        select(UsersORM)
        .limit(limit)
        .offset(offset)
    )
    # Выполняем запрос
    result = await session.scalars(query)
    # Преобразуем результат в список из словарей
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
    """
    SELECT * FROM users
    LIMIT limit OFFSET offset;
    """
    result =  await get_all_users_dto(session, limit=limit, page=page)
    return result

@get_session
async def add_user_db(
    user_name: str,
    session: AsyncSession = None
) -> List[UsersSchemaDTO]:
    """
    INSERT INTO users (name)
    VALUES (user_name);

    Т.к. есть функция get_all_users_dto,
    то выполнится ещё этот код:

    SELECT * FROM users;
    """
    user = UsersORM(name=user_name)
    session.add(user)
    await session.commit()
    result = await get_all_users_dto(session)
    return result

@get_session
async def add_all_users_db(
    user_names: List[str],
    session: AsyncSession = None
) -> List[UsersSchemaDTO]:
    """
    INSERT INTO users (name) 
    VALUES 
        ('user_name_1'),
        ('user_name_2'),
        ('user_name_3'),
        ...;

    SELECT * FROM users;
    """
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
    """
    DELETE FROM users
    WHERE id = id;

    SELECT * FROM users;
    """
    user = await session.get(UsersORM, id)
    if user:
        await session.delete(user)
        await session.commit()
        result = await get_all_users_dto(session)
        return result
    else:
        raise ValueError("There is no such ID")


async def main():
    """ Ну тасочки создаём крч. Тестить удобней """
    create_tables_task = asyncio.create_task(create_tables())
    await create_tables_task
    add_all_users_task = asyncio.create_task(add_all_users_db(["Misha", "Leva", "Nekit", "Ivan", "Grisha"]))
    get_all_users_task = asyncio.create_task(get_users_pagination_db())
    await add_all_users_task

    all_users = await get_all_users_task
    print(all_users)


if __name__ == "__main__":
    asyncio.run(main())