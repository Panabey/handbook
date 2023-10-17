from typing import Annotated

from fastapi import Query
from fastapi import Depends
from fastapi import APIRouter
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from routers.api.deps import get_async_session

from modules.database.orm.project_news import get_news
from modules.database.orm.project_news import get_all_news
from modules.database.orm.project_news import get_last_news

from modules.schemas.openapi import CACHE_HEADER
from modules.schemas.base import DetailInfo
from modules.schemas.project import NewsDetail
from modules.schemas.project import NewsAllDetail
from modules.schemas.project import NewsWidgetDetail


router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    "/news/widget",
    response_model=list[NewsWidgetDetail],
    summary="Краткое получение информации о новостном блоге проекта",
    openapi_extra=CACHE_HEADER
)  # fmt: skip
async def get_last_news_project(
    session: Session,
    limit: Annotated[int, Query(ge=1, le=8)] = 8,
):
    """
    **Параметры:**\n
    `limit` - Ограничение количества записей в ответе

    **Рекомендации!**\n
    Включить заголовок `X-Use-Cache: true` для использования кеширования.

    Если данные уже присутствовали в кеше, то получаемый заголовок в ответе:
    `X-Cache-Status: HIT`, в противном случае `X-Cache-Status: MISS`.
    """
    result = await get_last_news(session, limit)
    return result


@router.get(
    "/news/all",
    response_model=NewsAllDetail,
    summary="Получение информации о новостном блоге проекта"
)  # fmt: skip
async def get_all_news_project(
    session: Session,
    page: Annotated[int, Query(ge=1, le=10000)],
    limit: Annotated[int, Query(ge=5, le=20)] = 20,
):
    """
    **Параметры:**\n
    `page` - Страница с контентом\n
    `limit` - Ограничение записей на странице
    """
    result = await get_all_news(session, page, limit)
    return result


@router.get(
    "/news/",
    response_model=NewsDetail,
    summary="Получение страницы блога проекта",
    responses={404: {"model": DetailInfo}}
)  # fmt: skip
async def get_news_project(
    session: Session, news_id: Annotated[int, Query(ge=1, le=2147483647)]
):
    """
    **Параметры:**\n
    `news_id` - Уникальный числовой идентификатор блога проекта
    """
    result = await get_news(session, news_id)

    if not result:
        raise HTTPException(404, "Упс.. Мы ничего не смогли найти")
    return result
