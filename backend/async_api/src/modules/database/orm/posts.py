from sqlalchemy import select
from sqlalchemy.orm import defer
from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import Post


async def get_all_post(session: AsyncSession, continue_after: int, limit: int):
    smt = (
        select(Post)
        .order_by(Post.create_date.asc())
        .offset(continue_after)
        .limit(limit)
        .options(defer(Post.text), defer(Post.update_date))
    )
    result = await session.scalars(smt)
    return result.all()


async def get_post(session: AsyncSession, post_id: int):
    smt = select(Post).where(Post.id == post_id)

    result = await session.scalars(smt)
    return result.first()


async def search_post(
    session: AsyncSession, query: str, continue_after: int, limit: int
):
    smt = (
        select(Post)
        .where(Post.title.ilike(f"%{query}%"))
        .order_by(Post.create_date.asc())
        .offset(continue_after)
        .limit(limit)
        .options(defer(Post.text), defer(Post.update_date))
    )
    result = await session.scalars(smt)
    return result.all()
