from math import ceil

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import load_only
from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import ProjectNews


async def get_all_news(session: AsyncSession, page: int, limit: int):
    smt_page = select(func.count(ProjectNews.id))
    count = await session.scalar(smt_page)
    total_page = ceil(count / limit) if count else 0

    smt = (
        select(ProjectNews)
        .order_by(ProjectNews.create_date.desc())
        .limit(limit)
        .offset((page - 1) * limit)
        .options(
            load_only(
                ProjectNews.id,
                ProjectNews.title,
                ProjectNews.reading_time,
                ProjectNews.create_date,
            ),
        )
    )
    result = await session.scalars(smt)
    return {
        "items": result.unique().all(),
        "current_page": page,
        "total_page": total_page,
    }


async def get_last_news(session: AsyncSession, limit: int):
    smt = (
        select(ProjectNews)
        .order_by(ProjectNews.create_date.desc())
        .limit(limit)
        .options(
            load_only(ProjectNews.id, ProjectNews.title, ProjectNews.create_date),
        )
    )
    result = await session.scalars(smt)
    return result.all()


async def get_news(session: AsyncSession, news_id: int):
    smt = select(ProjectNews).where(ProjectNews.id == news_id)
    result = await session.scalars(smt)
    return result.first()
