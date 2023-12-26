from typing import Any

from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import User, OAuthService


async def exists_user_info(session: AsyncSession, user_id: int, service_name: str):
    smt = (
        select(User.id)
        .where(User.user_id == user_id, OAuthService.service_name == service_name)
        .options(User.service_info)
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


async def get_user_account(session: AsyncSession, user_id: int):
    smt = select(User).where(User.id == user_id).options(joinedload(User.service_info))

    result = await session.scalars(smt)
    return result.first()
