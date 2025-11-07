from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from typing import Annotated
import datetime

from base import Base


intpk = Annotated[int, mapped_column(autoincrement=True, primary_key=True)]
str_16 = Annotated[str, mapped_column(String(16), nullable=False)]
created_at = Annotated[str, mapped_column(default=datetime.datetime.utcnow())]
updated_at = Annotated[str, mapped_column(default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())]


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    name: Mapped[str_16]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]