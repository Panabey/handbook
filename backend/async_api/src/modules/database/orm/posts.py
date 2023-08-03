from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import Posts


async def get_post(session: AsyncSession, post_id: int):
    smt = select(Posts).where(Posts.id == post_id)

    result = await session.scalars(smt)
    return result.first()
