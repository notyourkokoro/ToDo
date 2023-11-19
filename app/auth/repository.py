from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User


async def del_me(user: User, session: AsyncSession) -> None:
    await session.delete(user)
    await session.commit()
