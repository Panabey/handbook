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

from modules.schemas.openapi import CACHE_HEADER
from modules.schemas.base import DetailInfo
from modules.schemas.handbook import PageDetail
from modules.schemas.handbook import SearchDetail
from modules.schemas.handbook import ContentDetail
from modules.schemas.handbook import CategoryDetail
from modules.schemas.handbook import SearchPageDetail

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_async_session)]
Int = Annotated[int, Query(ge=1, le=2147483647)]


@router.get(
    "/all",
    response_model=list[CategoryDetail],
    summary="Получение списка доступных справочников",
    openapi_extra=CACHE_HEADER
)  # fmt: skip
async def get_handbooks(session: Session):
    """
    **Рекомендации!**\n
    Включить заголовок `X-Use-Cache: true` для использования кеширования.

    Если данные уже присутствовали в кеше, то получаемый заголовок в ответе:
    `X-Cache-Status: HIT`, в противном случае `X-Cache-Status: MISS`.
    """
    result = await get_all(session)
    return result


@router.get(
    "/content",
    response_model=ContentDetail,
    summary="Получение содержимого справочника",
    openapi_extra=CACHE_HEADER,
    responses={404: {"model": DetailInfo}}
)  # fmt: skip
async def get_content_handbook(
    session: Session,
    handbook: Annotated[str, Query(min_length=1, max_length=80)],
):
    """
    **Параметры:**\n
    `handbook` - название справочника (разрешено использование пробелов)

    Полученный контент приходит в сортированном виде!

    **Рекомендации!**\n
    Включить заголовок `X-Use-Cache: true` для использования кеширования.

    Если данные уже присутствовали в кеше, то получаемый заголовок в ответе:
    `X-Cache-Status: HIT`, в противном случае `X-Cache-Status: MISS`.
    """
    result, book = await get_content(session, handbook)
    if not result:
        raise HTTPException(404, "По Вашему запросу ничего не найдено..")

    result.book_info = book.book_info
    # Сортировка тем и подтем от меньшего к большему
    result.content.sort(key=lambda x: x.part)

    for content_item in result.content:
        content_item.hbook_page.sort(key=lambda x: x.subpart)
    return result


@router.get(
    "",
    response_model=PageDetail,
    summary="Получение страницы справочника",
    openapi_extra=CACHE_HEADER,
    responses={404: {"model": DetailInfo}}
)  # fmt: skip
async def get_page_handbook(session: Session, page_id: Int):
    """
    **Параметры:**\n
    `page_id` - Уникальный числовой идентификатор страницы справочника

    **Рекомендации!**\n
    Включить заголовок `X-Use-Cache: true` для использования кеширования.

    Если данные уже присутствовали в кеше, то получаемый заголовок в ответе:
    `X-Cache-Status: HIT`, в противном случае `X-Cache-Status: MISS`.
    """
    result = await get_page_by_id(session, page_id)
    if not result:
        raise HTTPException(404, "По Вашему запросу ничего не найдено..")
    return result


@router.post(
    "/search",
    response_model=list[SearchPageDetail],
    summary="Поиск по содержимому справочника"
)  # fmt: skip
async def search_page_handbook(session: Session, schema: SearchDetail):
    """
    **Параметры:**\n
    `q` - Текст для поиска по названию страницы справочника (не зависит от регистра)\n
    `handbook_id` - Числовой уникальный идентификатор справочника\n
    `limit` - Ограничение количества записей в ответе\n
    `continue_after` - Числовой идентифкикатор для продолжения с конкретной записи
    """
    result = await search_page(
        session, schema.handbook_id, schema.q, schema.limit, schema.continue_after
    )
    return result
