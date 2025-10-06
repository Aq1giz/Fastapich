from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Annotated
import datetime

from base import Base


str16 = Annotated[str, mapped_column(String(16), nullable=False)]
created_at = Annotated[datetime.datetime, mapped_column(default=datetime.datetime.utcnow)]
updated_at = Annotated[datetime.datetime, mapped_column(nullable=True, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)]


class BooksORM(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str16]
    author: Mapped[str16]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]