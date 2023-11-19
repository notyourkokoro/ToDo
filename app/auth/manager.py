from typing import Optional

from fastapi import Depends

from fastapi_users import BaseUserManager, IntegerIDMixin, models, FastAPIUsers
from starlette.requests import Request
from starlette.responses import Response

from app.auth.config import auth_backend
from app.auth.models import User, get_user_db
from app.config import settings
from app.logger import logger


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.secret_auth
    verification_token_secret = settings.secret_auth

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ) -> None:
        logger.info(f'New User with id {user.id} has registered')

    async def on_after_login(
        self,
        user: models.UP,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ) -> None:
        logger.info(f'User with id {user.id} has login')


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
