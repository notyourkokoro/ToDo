from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.manager import current_user
from app.auth.models import User
from app.auth.repository import del_me
from app.database import db

router = APIRouter(tags=['Users'])


@router.delete('/me', status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(db.get_async_session),
) -> None:
    await del_me(user=user, session=session)
