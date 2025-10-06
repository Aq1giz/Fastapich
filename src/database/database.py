from sqlalchemy.ext.asyncio import AsyncSession
from base import async_session_fabric
from base import async_engine
from models.books import Base
from models.books import BooksORM
import asyncio

def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session_fabric() as session:
            try:
                return await func(*args, session=session, **kwargs)
            except Exception as e_:
                await session.rollback()
                raise e_
            finally:
                await session.close()

    return wrapper
    

async def create_table():
    async with async_engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@connection
async def add_book(title: str, author: str, session: AsyncSession):
    book = BooksORM(title=title, author=author)
    session.add(book)
    await session.commit()