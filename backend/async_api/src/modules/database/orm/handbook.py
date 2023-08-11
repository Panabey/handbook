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
    )

    result = await session.execute(smt)
    return result.all()


async def get_content(session: AsyncSession, handbook_id: int):
    smt = (
        select(HBook)
        .join(HBook.content)
        .join(HBookContent.hbook_page)
        .where(HBook.id == handbook_id, HBookContent.is_visible)
        .options(
            load_only(HBook.id, HBook.title, HBook.description),
            joinedload(HBook.content)
            .load_only(HBookContent.title)
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
        .options(defer(HBookPage.is_visible), defer(HBookPage.handbook_title_id))
    )

    result = await session.scalars(smt)
    return result.first()
