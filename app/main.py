import uvicorn

from fastapi import FastAPI

from app.auth.manager import fastapi_users
from app.auth.config import auth_backend
from app.auth.schemas import UserRead, UserCreate, UserUpdate

from app.auth.router import router as user_router
from app.todo.router import router as todo_router

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    user_router,
    prefix='/users',
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)

app.include_router(
    todo_router,
    prefix='/todo',
)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
