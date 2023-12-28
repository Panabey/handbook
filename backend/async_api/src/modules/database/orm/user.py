from typing import Any

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import insert
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import contains_eager
from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import User, OAuthService


async def exists_user_info(session: AsyncSession, user_id: int, service_name: str):
    smt = (
        select(User)
        .join(User.service_info)
        .where(User.user_id == user_id, OAuthService.service_name == service_name)
        .options(contains_eager(User.service_info))
    )
    result = await session.scalars(smt)
    return result.first()


async def get_user_info(session: AsyncSession, **kwargs: dict[str, Any]):
    smt = select(User).filter_by(**kwargs)
    result = await session.scalars(smt)
    return result.first()


async def create_user(session: AsyncSession, **kwargs: dict[str, Any]):
    smt = insert(User).values(**kwargs).returning(User)
    result = await session.scalars(smt)
    return result.first()


async def update_user(session: AsyncSession, user_id: int, **kwargs: dict[str, Any]):
    smt = update(User).where(User.id == user_id).values(**kwargs).returning(User)
    result = await session.scalars(smt)
    return result.first()


async def get_user_account(session: AsyncSession, user_id: int, short: bool = False):
    smt = select(User).where(User.id == user_id)
    if not short:
        smt = smt.options(joinedload(User.service_info))
    result = await session.scalars(smt)
    return result.first()
