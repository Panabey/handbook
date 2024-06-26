from math import ceil

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import defer
from sqlalchemy.orm import contains_eager
from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import Article, Tag


async def get_all_article(session: AsyncSession, page: int, limit: int):
    smt_page = select(func.count(Article.id))
    count = await session.scalar(smt_page)
    total_page = ceil(count / limit) if count else 0

    subquery = (
        select(Article.id)
        .order_by(Article.create_date.desc())
        .limit(limit)
        .offset((page - 1) * limit)
        .subquery()
    )

    smt = (
        select(Article)
        .join(subquery, Article.id == subquery.c.id)
        .join(Article.tags_article_info, isouter=True)
        .order_by(Article.create_date.desc())
        .options(
            defer(Article.text),
            defer(Article.update_date),
            contains_eager(Article.tags_article_info).defer(Tag.status_id),
        )
    )
    result = await session.scalars(smt)
    return {
        "items": result.unique().all(),
        "current_page": page,
        "total_page": total_page,
    }


async def get_article(session: AsyncSession, post_id: int):
    smt = (
        select(Article)
        .join(Article.tags_article_info, isouter=True)
        .where(Article.id == post_id)
        .options(
            contains_eager(Article.tags_article_info).defer(Tag.status_id),
        )
    )

    result = await session.scalars(smt)
    return result.first()


async def search_article(
    session: AsyncSession,
    query: str | None,
    tags_id: list[int],
    continue_after: int | None,
    limit: int,
):
    subquery = (
        select(Article.id)
        .order_by(Article.create_date.desc())
        .limit(limit)
        .offset(continue_after)
    )

    if query:
        subquery = subquery.where(Article.title.ilike(f"%{query}%"))
    subquery = subquery.subquery()

    smt = (
        select(Article)
        .join(subquery, Article.id == subquery.c.id)
        .join(Article.tags_article_info, isouter=True)
        .order_by(Article.create_date.desc())
        .options(
            defer(Article.text),
            defer(Article.update_date),
            contains_eager(Article.tags_article_info).defer(Tag.status_id),
        )
    )
    if tags_id:
        smt = smt.where(Tag.id.in_(tags_id))

    result = await session.scalars(smt)
    return result.unique().all()
