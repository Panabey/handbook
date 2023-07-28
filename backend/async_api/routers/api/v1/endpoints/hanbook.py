from typing import Annotated

from fastapi import Depends
from fastapi import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from routers.api.deps import get_async_session
from modules.database.orm.handbook import get_all
from modules.database.orm.handbook import get_content


router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_async_session)]


@router.get("/all")
async def get_handbooks(session: Session):
    result = await get_all(session)
    return [value._mapping for value in result]


@router.get("/content")
async def get_content_handbook(session: Session):
    result = await get_content(session)
    return [value for value in result]


@router.get("/")
async def get_page_handbook():
    pass
