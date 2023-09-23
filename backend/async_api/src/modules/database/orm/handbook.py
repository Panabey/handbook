from sqlalchemy import select
from sqlalchemy.orm import defer
from sqlalchemy.orm import load_only
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import contains_eager
from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import Handbook as HBook
from modules.database.models import HandbookPage as HBookPage
from modules.database.models import HandbookContent as HBookContent
from modules.database.models import HandbookСategory as HBookCategory


async def get_all(session: AsyncSession):
    smt = (
        select(HBookCategory)
        .join(HBookCategory.hbook_category)
        .join(HBook.status_info, isouter=True)
        .where(HBook.is_visible)
        .order_by(HBook.id, HBookCategory.id)
        .options(
            contains_eager(HBookCategory.hbook_category)
            .load_only(HBook.id, HBook.title, HBook.logo_url)
            .contains_eager(HBook.status_info),
        )
    )

    result = await session.scalars(smt)
    return result.unique().all()


async def get_content(session: AsyncSession, handbook_title: str):
    smt = (
        select(HBook)
        .where(HBook.title.ilike(handbook_title), HBook.is_visible)
        .options(
            load_only(HBook.id, HBook.title, HBook.description),
            joinedload(HBook.content)
            .load_only(HBookContent.title, HBookContent.description)
            .joinedload(HBookContent.hbook_page)
            .load_only(HBookPage.id, HBookPage.title),
        )
    )

    result = await session.scalars(smt)
    return result.first()


async def get_page_by_id(session: AsyncSession, page_id: int):
    smt = (
        select(HBookPage)
        .join(HBookPage.hbook_content)
        .join(HBookContent.hbook)
        .where(HBookPage.id == page_id, HBook.is_visible)
        .options(
            defer(HBookPage.content_id),
            contains_eager(HBookPage.hbook_content)
            .load_only(HBookContent.id)
            .contains_eager(HBookContent.hbook)
            .load_only(HBook.id, HBook.title),
        )
    )

    result = await session.scalars(smt)
    return result.first()


async def search_page(
    session: AsyncSession,
    handbook_id: int | None,
    search_text: str,
    limit: int,
    continue_after: int | None,
):
    smt = (
        select(
            HBook.id,
            HBook.title,
            HBookPage.id.label("page_id"),
            HBookPage.title.label("page_title"),
        )
        .join(HBook.content)
        .join(HBookContent.hbook_page)
        .where(HBookPage.title.ilike(f"%{search_text}%"), HBook.is_visible)
        .order_by(HBookPage.id)
        .offset(continue_after)
        .limit(limit)
    )
    if handbook_id:
        smt = smt.where(HBook.id == handbook_id)

    result = await session.execute(smt)
    return result.all()
