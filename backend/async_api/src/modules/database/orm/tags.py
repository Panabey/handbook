from sqlalchemy import select
from sqlalchemy.orm import contains_eager
from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import Tag, TagStatus


async def get_tags(session: AsyncSession, title: str, limit: int):
    smt = (
        select(TagStatus)
        .join(TagStatus.tag_info)
        .where(TagStatus.title.ilike(title))
        .order_by(Tag.id)
        .limit(limit)
        .options(contains_eager(TagStatus.tag_info).load_only(Tag.id, Tag.title))
    )

    result = await session.scalars(smt)
    tags = result.unique().first()
    if tags:
        return tags.tag_info
    return None
