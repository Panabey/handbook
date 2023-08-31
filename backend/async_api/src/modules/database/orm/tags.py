from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import Tag, TagStatus


async def get_tags(session: AsyncSession, title: str, limit: int):
    smt = (
        select(TagStatus)
        .where(TagStatus.title.ilike(title))
        .order_by(Tag.id)
        .limit(limit)
        .options(joinedload(TagStatus.tag_info))
    )

    result = await session.scalars(smt)
    tags = result.unique().first()
    if tags:
        return tags.tag_info
    return None
