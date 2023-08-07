from sqlalchemy import select
from sqlalchemy.orm import defer
from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import Posts


async def get_all_post(session: AsyncSession, continue_after: int, limit: int):
    smt = (
        select(Posts)
        .order_by(Posts.create_date.asc())
        .offset(continue_after)
        .limit(limit)
        .options(defer(Posts.text), defer(Posts.update_date))
    )
    result = await session.scalars(smt)
    return result.all()


async def get_post(session: AsyncSession, post_id: int):
    smt = select(Posts).where(Posts.id == post_id)

    result = await session.scalars(smt)
    return result.first()


async def search_post(
    session: AsyncSession, query: str, continue_after: int, limit: int
):
    smt = (
        select(Posts)
        .where(Posts.title.ilike(f"%{query}%"))
        .order_by(Posts.create_date.asc())
        .offset(continue_after)
        .limit(limit)
        .options(defer(Posts.text), defer(Posts.update_date))
    )
    result = await session.scalars(smt)
    return result.all()
