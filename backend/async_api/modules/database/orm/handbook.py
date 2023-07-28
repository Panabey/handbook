from sqlalchemy import select
from sqlalchemy.orm import load_only, selectinload

from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import Handbook as HBook
from modules.database.models import HandbookPage as HBookPage
from modules.database.models import HandbookContent as HBookContent


async def get_all(session: AsyncSession):
    smt = select(HBook.id, HBook.title, HBook.description)\
        .where(HBook.is_visible)  # fmt: skip

    handbooks = await session.execute(smt)
    return handbooks.all()


async def get_content(session: AsyncSession):
    smt = (
        select(HBookContent)
        .join(HBookContent.hbook_page)
        .options(
            load_only(HBookContent.id, HBookContent.title),
            selectinload(HBookContent.hbook_page).load_only(
                HBookPage.id, HBookPage.title, HBookPage.slug
            ),
        )
        .distinct(HBookContent.id, HBookContent.title)
    )

    content = await session.scalars(smt)
    return content.all()


async def get_page(session: AsyncSession):
    pass
