from typing import Annotated

from fastapi import Query
from fastapi import Depends
from fastapi import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from routers.api.deps import get_async_session
from modules.database.orm.handbook import get_all
from modules.database.orm.handbook import get_content
from modules.database.orm.handbook import get_page_by_id

from modules.schemas.handbook import PageDetail
from modules.schemas.handbook import ContentDetail
from modules.schemas.handbook import HandbookDetail

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_async_session)]
Id = Annotated[int, Query(ge=1, le=2147483647)]


@router.get("/all", response_model=list[HandbookDetail])
async def get_handbooks(session: Session):
    """Получение списка всех доступных справочников"""
    result = await get_all(session)
    return result


@router.get("/content", response_model=ContentDetail)
async def get_content_handbook(session: Session, handbook_id: Id):
    """Получение списка всех тем и подтем справочника"""
    result = await get_content(session, handbook_id)
    return result


@router.get("/", response_model=PageDetail)
async def get_page_handbook(session: Session, page_id: Id):
    """Получение содержимого подтемы справочника"""
    result = await get_page_by_id(session, page_id)
    return result
