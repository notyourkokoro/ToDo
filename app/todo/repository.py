from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.todo.models import ToDo
from app.todo.schemas import ToDoCreate, ToDoUpdate


async def get_todos(user_id: int, session: AsyncSession) -> list[ToDo]:
    query = select(ToDo).where(ToDo.creator_id == user_id)
    result: Result = await session.execute(query)
    todos = result.scalars().all()
    return list(todos)


async def get_todo(todo_id: int, session: AsyncSession) -> ToDo | None:
    query = select(ToDo).where(ToDo.id == todo_id)
    result: Result = await session.execute(query)
    return result.scalar()


async def add_todo(user_id: int, todo_in: ToDoCreate, session: AsyncSession) -> ToDo:
    todo: ToDo = ToDo(creator_id=user_id, **todo_in.model_dump())
    session.add(todo)
    await session.commit()
    return todo


async def update_todo(todo: ToDo, todo_update: ToDoUpdate, session: AsyncSession, exclude_unset: bool = False) -> ToDo:
    for attr, val in todo_update.model_dump(exclude_unset=exclude_unset).items():
        setattr(todo, attr, val)
    await session.commit()
    return todo


async def del_todo(todo: ToDo, session: AsyncSession) -> None:
    await session.delete(todo)
    await session.commit()
