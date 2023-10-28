from typing import Annotated

from fastapi import Query
from fastapi import Depends
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from routers.api.deps import get_async_session
from modules.database.orm.tags import get_tags

from modules.schemas.openapi import CACHE_HEADER
from modules.schemas.base import DetailInfo
from modules.schemas.tags import TagsDetail


router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    "",
    response_model=list[TagsDetail],
    summary="Получение списка тегов",
    openapi_extra=CACHE_HEADER,
    responses={404: {"model": DetailInfo}}
)  # fmt: skip
async def get_all_tags(
    session: Session,
    status: Annotated[str, Query(min_length=1, max_length=60)],
    limit: Annotated[int, Query(ge=1, le=15)] = 15,
):
    """
    **Параметры:**\n
    `status` - Статус тег, который разделяется на следующие константные группы:\n
    - `article` - Группа тегов для статей\n
    - `quiz` - Группа тегов для квизов\n
    `limit` -  Ограничение количества записей в ответе

    **Рекомендации!**\n
    Включить заголовок `X-Use-Cache: true` для использования кеширования.

    Если данные уже присутствовали в кеше, то получаемый заголовок в ответе:
    `X-Cache-Status: HIT`, в противном случае `X-Cache-Status: MISS`.
    """
    result = await get_tags(session, status, limit)
    if result is None:
        raise HTTPException(404, "По Вашему запросу ничего не найдено..")
    return result
