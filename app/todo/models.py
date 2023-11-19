from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base import Base

if TYPE_CHECKING:
    from app.auth.models import User


class ToDo(Base):
    __tablename__ = 'todo'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    title: Mapped[str] = mapped_column(String(25))
    description: Mapped[str | None]

    user_rel: Mapped['User'] = relationship(back_populates='todos_rel', passive_deletes=True)

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'
