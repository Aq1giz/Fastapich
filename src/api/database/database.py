from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from functools import wraps
from typing import List, Optional
from .. import UsersSchemaDTO
from .models.users import UsersORM
import asyncio

from . import Base, engine, session_fabric


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
            except Exception as ex:
                await session.rollback()
                raise ValueError(str(ex))
    return wrapper


async def get_all_users_dto(
    session: AsyncSession,
    limit: Optional[int] = None,
    page: Optional[int] = None,
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
        .order_by(UsersORM.id)
    )
    # Выполняем запрос
    result = await session.scalars(query)
    # Преобразуем результат в список из словарей
    result_dto = [UsersSchemaDTO.model_validate(row, from_attributes=True) for row in result]
    return result_dto


@get_session
async def get_user_by_id(
    user_id: int,
    session: AsyncSession,
) -> UsersSchemaDTO:
    """
    SELECT * FROM users
    WHERE id = user_id;
    """
    query = (
        select(UsersORM)
        .where(UsersORM.id == user_id)
    )
    result = await session.execute(query)
    result = result.one()
    result_dto = [UsersSchemaDTO.model_validate(row, from_attributes=True) for row in result]
    return result_dto



# @get_session
# async def get_last_user_id(
#     session: AsyncSession
# ):
#     id_list = await session.scalars(select(UsersORM.id))
#     return id_list[-1]


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
    username: str,
    password: str,
    session: AsyncSession = None
) -> UsersORM:
    """
    INSERT INTO users (username)
    VALUES (user_name);

    Т.к. есть функция get_all_users_dto,
    то выполнится ещё этот код:

    SELECT * FROM users;
    """
    user = UsersORM(username=username, password=password)
    session.add(user)
    await session.commit()
    return user

@get_session
async def add_all_users_db(
    usernames: List[str],
    passwords: List[str],
    session: AsyncSession = None
) -> List[UsersSchemaDTO]:
    """
    INSERT INTO users (username) 
    VALUES 
        ('user_name_1'),
        ('user_name_2'),
        ('user_name_3'),
        ...;

    SELECT * FROM users;
    """
    users_list = [UsersORM(username=username, password=password) for username, password in zip(usernames, passwords)]
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
    

@get_session
async def update_user_db(
    user_id: int,
    new_username: str,
    session: AsyncSession = None
) -> List[UsersSchemaDTO]:
    """
    UPDATE users
    SET username = 'Aksjdfsjf', password = 'ksalsadsfk'
    WHERE id=id;
    """
    user = await session.get(UsersORM, user_id)

    if not user:
        raise ValueError("There is no such ID")
    elif user.username == new_username:
        return user
    else:
        user.username = new_username
        await session.commit()
        result = await get_user_by_id(user_id)
        return result


async def main():
    create_tables_task = asyncio.create_task(create_tables())
    await create_tables_task
    add_all_users_task = asyncio.create_task(add_all_users_db(
            usernames=["Misha", "Leva", "Nekit", "Ivan", "Grisha"],
            passwords=["qwerty123", "123432111", "34596382", "fsjiedof", "324dfd32"]))
    update_user_task = asyncio.create_task(update_user_db(user_id=3, new_username="Fsflajskf"))
    await add_all_users_task
    await update_user_task

    get_all_users_task = asyncio.create_task(get_users_pagination_db())
    all_users = await get_all_users_task
    print(all_users)


    
if __name__ == "__main__":
    asyncio.run(main())