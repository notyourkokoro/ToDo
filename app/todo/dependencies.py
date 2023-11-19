from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.manager import current_user
from app.auth.models import User
from app.database import db
from app.todo.models import ToDo
from app.todo.repository import get_todo


async def todo_by_id(
        todo_id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(db.get_async_session),
) -> ToDo:
    todo = await get_todo(todo_id=todo_id, session=session)

    if user.id != todo.creator_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You don’t have permission to access'
        )

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Record not found'
        )

    return todo
