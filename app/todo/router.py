from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.database import db
from app.auth.manager import current_user
from app.todo.models import ToDo
from app.todo.schemas import ToDoRead, ToDoCreate, ToDoUpdate
from app.todo.repository import add_todo, get_todos, update_todo, del_todo
from app.todo.dependencies import todo_by_id

router = APIRouter(tags=['ToDo'])


@router.post('/create', response_model=ToDoRead, status_code=status.HTTP_201_CREATED)
async def create_todo(
        todo: ToDoCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(db.get_async_session),
):
    todo = await add_todo(user_id=user.id, todo_in=todo, session=session)
    return todo


@router.get('/me_todos', response_model=list[ToDoRead])
async def read_todos(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(db.get_async_session),
):
    todos = await get_todos(user_id=user.id, session=session)

    if not todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Records not found'
        )

    return todos


@router.get('/{todo_id}', response_model=ToDoRead)
async def read_todo(
        todo: ToDoRead = Depends(todo_by_id),
):
    return todo


@router.patch('/update/{todo_id}', response_model=ToDoRead)
async def patch_todo(
        todo_update: ToDoUpdate,
        todo: ToDo = Depends(todo_by_id),
        session: AsyncSession = Depends(db.get_async_session),
):
    return await update_todo(
        todo=todo,
        todo_update=todo_update,
        session=session,
        exclude_unset=True,
    )


@router.delete('/delete/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
        todo: ToDo = Depends(todo_by_id),
        session: AsyncSession = Depends(db.get_async_session),
) -> None:
    await del_todo(todo=todo, session=session)
