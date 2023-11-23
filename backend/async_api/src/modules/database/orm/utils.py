from sqlalchemy import select
from sqlalchemy.orm import load_only, contains_eager
from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import HandbookPage, Article, HandbookContent, Handbook


async def sitemap_data(session: AsyncSession):
    handbooks = (
        select(HandbookPage)
        .join(HandbookPage.hbook_content)
        .join(HandbookContent.hbook)
        .where(Handbook.is_visible)
        .limit(10000)
        .options(
            load_only(HandbookPage.id, HandbookPage.title, HandbookPage.update_date),
            contains_eager(HandbookPage.hbook_content)
            .load_only(HandbookContent.id)
            .contains_eager(HandbookContent.hbook)
            .load_only(Handbook.slug, Handbook.title),
        )
    )
    handbook_result = await session.scalars(handbooks)

    articles = (
        select(Article)
        .limit(10000)
        .options(load_only(Article.id, Article.title, Article.update_date))
    )
    article_result = await session.scalars(articles)
    return {"handbooks": handbook_result.all(), "articles": article_result.all()}
