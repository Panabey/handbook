from typing import Annotated

from fastapi import Query
from fastapi import Depends
from fastapi import APIRouter
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from routers.api.deps import get_async_session
from modules.database.orm.articles import get_article
from modules.database.orm.articles import search_article
from modules.database.orm.articles import get_all_article

from modules.schemas.base import DetailInfo
from modules.schemas.articles import SearchDetail
from modules.schemas.articles import ArticleDetail
from modules.schemas.articles import ArticleAllDetail
from modules.schemas.articles import ArticleShortDetail

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    "/all",
    response_model=ArticleAllDetail,
    summary="Получение полного списка новостей"
)  # fmt: skip
async def get_all_articles(
    session: Session,
    page: Annotated[int, Query(ge=1, le=10000)],
    limit: Annotated[int, Query(ge=5, le=20)] = 20,
):
    """
    Вывод представляет собой неполную информацию о статье.
    """
    result = await get_all_article(session, page, limit)
    return result


@router.get(
    "/",
    response_model=ArticleDetail,
    summary="Получение информации о конкрентной новости",
    responses={404: {"model": DetailInfo}}
)  # fmt: skip
async def get_page_article(
    session: Session, article_id: Annotated[int, Query(ge=1, le=2147483647)]
):
    """Получение полной ифнормации о странице, за исключением
    логотипа страницы.
    """
    result = await get_article(session, article_id)
    if not result:
        raise HTTPException(404, "Данный пост не существует")
    return result


@router.post(
    "/search",
    response_model=list[ArticleShortDetail],
    summary="Поиск по статьям",
    responses={400: {"model": DetailInfo}}
)  # fmt: skip
async def get_search_article(session: Session, schema: SearchDetail):
    """Поиск по названию статьи (Включая теги)"""
    if not schema.q and not schema.tags:
        raise HTTPException(400, "Одно из обязательных полей пустое..")

    result = await search_article(
        session, schema.q, schema.tags, schema.continue_after, schema.limit
    )
    return result
