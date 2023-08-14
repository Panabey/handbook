from sqlalchemy import select
from sqlalchemy.orm import load_only, defer, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import Status
from modules.database.models import Handbook as HBook
from modules.database.models import HandbookPage as HBookPage
from modules.database.models import HandbookContent as HBookContent


async def get_all(session: AsyncSession):
    smt = (
        select(
            HBook.id, HBook.title, HBook.description, HBook.logo_url,
            Status.title.label("status")  # fmt: skip
        )
        .join(HBook.status_info, isouter=True)
        .where(HBook.is_visible)
        .order_by(HBook.id)
    )

    result = await session.execute(smt)
    return result.all()


async def get_content(session: AsyncSession, handbook_id: int):
    smt = (
        select(HBook)
        .where(HBook.id == handbook_id, HBookContent.is_visible)
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
        .where(HBookPage.id == page_id, HBookPage.is_visible)
        .options(defer(HBookPage.is_visible), defer(HBookPage.content_id))
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
