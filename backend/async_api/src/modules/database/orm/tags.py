from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import Tag


async def get_tags(session: AsyncSession, limit: int):
    smt = select(Tag).order_by(Tag.id).limit(limit)

    result = await session.scalars(smt)
    return result.all()
