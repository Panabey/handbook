from sqlalchemy import select
from sqlalchemy.orm import load_only, selectinload, defer

from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import Handbook as HBook
from modules.database.models import HandbookPage as HBookPage
from modules.database.models import HandbookContent as HBookContent


async def get_all(session: AsyncSession):
    smt = select(HBook.id, HBook.title, HBook.description)\
        .where(HBook.is_visible)  # fmt: skip

    handbooks = await session.execute(smt)
    return handbooks.all()


async def get_content(session: AsyncSession, handbook_id: int):
    smt = (
        select(HBookContent)
        .join(HBookContent.hbook_page)
        .where(HBookContent.handbook_id == handbook_id, HBookContent.is_visible)
        .options(
            load_only(HBookContent.id, HBookContent.title),
            selectinload(HBookContent.hbook_page).load_only(
                HBookPage.id, HBookPage.title, HBookPage.slug
            ),
        )
        .distinct(HBookContent.id)
    )

    result = await session.scalars(smt)
    return result.all()


async def get_page_by_id(session: AsyncSession, page_id: int):
    smt = (
        select(HBookPage)
        .where(HBookPage.id == page_id, HBookPage.is_visible)
        .options(defer(HBookPage.is_visible), defer(HBookPage.handbook_title_id))
    )

    result = await session.scalars(smt)
    return result.first()
