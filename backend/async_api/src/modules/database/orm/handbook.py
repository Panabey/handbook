from sqlalchemy import select
from sqlalchemy.orm import defer
from sqlalchemy.orm import load_only
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import contains_eager
from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import Handbook as HBook
from modules.database.models import HandbookPage as HBookPage
from modules.database.models import HandbookContent as HBookContent


async def get_all(session: AsyncSession):
    smt = (
        select(HBook)
        .join(HBook.status_info, isouter=True)
        .order_by(HBook.id)
        .options(
            load_only(HBook.id, HBook.title, HBook.logo_url),
            contains_eager(HBook.status_info),
        )
    )

    result = await session.scalars(smt)
    return result.all()


async def get_content(session: AsyncSession, handbook_title: str):
    smt = (
        select(HBook)
        .where(HBook.title.ilike(handbook_title))
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
        .where(HBookPage.id == page_id)
        .options(
            defer(HBookPage.content_id),
            joinedload(HBookPage.hbook_content)
            .load_only(HBookContent.id)
            .joinedload(HBookContent.hbook)
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
        .where(HBookPage.title.ilike(f"%{search_text}%"))
        .order_by(HBookPage.id)
        .offset(continue_after)
        .limit(limit)
    )
    if handbook_id:
        smt = smt.where(HBook.id == handbook_id)

    result = await session.execute(smt)
    return result.all()
