from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

URL = "sqlite+aiosqlite:///database.db"

async_engine = create_async_engine(url=URL, echo=True)
async_session_fabric = async_sessionmaker(bind=async_engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass