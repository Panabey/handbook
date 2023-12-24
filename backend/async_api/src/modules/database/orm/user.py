from typing import Any

from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import User, OAuthService


async def exists_user_info(session: AsyncSession, user_id: int, service_name: str):
    smt = (
        select(User)
        .join(OAuthService)
        .where(User.user_id == user_id, OAuthService.service_name == service_name)
    )
    result = await session.scalars(smt)
    return result.first()


async def get_user_info(session: AsyncSession, **kwargs: dict[str, Any]):
    smt = select(User).filter_by(**kwargs)
    result = await session.scalars(smt)
    return result.first()


async def create_user(session: AsyncSession, **kwargs: dict[str, Any]):
    smt = insert(User).values(**kwargs).returning(User.id)
    result = await session.scalars(smt)
    return result.first()
