from typing import TYPE_CHECKING

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


from app.base import Base
from app.database import db

if TYPE_CHECKING:
    from app.todo.models import ToDo


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)

    todos_rel: Mapped[list['ToDo']] = relationship(back_populates='user_rel', cascade='all, delete')


async def get_user_db(session: AsyncSession = Depends(db.get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
