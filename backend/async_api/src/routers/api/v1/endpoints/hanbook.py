import re
from typing import Annotated

from fastapi import Query
from fastapi import Depends
from fastapi import APIRouter
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from routers.api.deps import get_async_session
from modules.database.orm.handbook import get_all
from modules.database.orm.handbook import get_content
from modules.database.orm.handbook import get_page_by_id
from modules.database.orm.handbook import search_page

from modules.schemas.base import DetailInfo
from modules.schemas.handbook import PageDetail
from modules.schemas.handbook import SearchDetail
from modules.schemas.handbook import ContentDetail
from modules.schemas.handbook import CategoryDetail
from modules.schemas.handbook import SearchPageDetail

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_async_session)]
Int = Annotated[int, Query(ge=1, le=2147483647)]


@router.get("/all", response_model=list[CategoryDetail])
async def get_handbooks(session: Session):
    """Получение списка всех доступных категорий и их справочников"""
    result = await get_all(session)
    return result


@router.get(
    "/content",
    response_model=ContentDetail,
    responses={404: {"model": DetailInfo}}
)  # fmt: skip
async def get_content_handbook(
    session: Session, handbook: Annotated[str, Query(min_length=1, max_length=80)]
):
    """Получение списка всех тем и подтем справочника.

    Полученнные данные (темы) приходят в сортированном виде,
    делать что то дополнительно не требуется.
    """
    handbook = re.sub(r"[-\s]+", " ", handbook.strip())

    result = await get_content(session, handbook)
    if not result:
        raise HTTPException(404, "По Вашему запросу ничего не найдено..")

    # сортировка тем и подтем от меньшего к большему
    result.content.sort(key=lambda x: x.part)

    for content_item in result.content:
        content_item.hbook_page.sort(key=lambda x: x.subpart)
    return result


@router.get(
    "/",
    response_model=PageDetail,
    responses={404: {"model": DetailInfo}}
)  # fmt: skip
async def get_page_handbook(session: Session, page_id: Int):
    """Получение содержимого подтемы справочника.

    Полученный текст представлен в виде Markdown v2
    """
    result = await get_page_by_id(session, page_id)
    if not result:
        raise HTTPException(404, "По Вашему запросу ничего не найдено..")
    return result


@router.post("/search", response_model=list[SearchPageDetail])
async def search_page_handbook(session: Session, schema: SearchDetail):
    """Поиск тем по конкретному справочнику или по всем записям.

    Лимит установлен на 15 строк. Чтобы продолжить список
    требуется указать полю continue_after с какой записи продолжить. В теории :)
    """
    result = await search_page(
        session, schema.handbook_id, schema.q, schema.limit, schema.continue_after
    )
    return result
