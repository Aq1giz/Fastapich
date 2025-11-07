from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


URL = "postgresql+psycopg://postgres:postgres@localhost/postgres"

engine = create_async_engine(url=URL, echo=True)
session_fabric = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    def __repr__(self):
        pass