from typing import Annotated

from fastapi import Query
from fastapi import Depends
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from routers.api.deps import get_async_session
from modules.database.orm.tags import get_tags

from modules.schemas.base import DetailInfo
from modules.schemas.quiz import TagsDetail


router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    "/", response_model=list[TagsDetail], responses={404: {"model": DetailInfo}}
)
async def get_all_tags(
    session: Session,
    title_status: Annotated[str, Query(min_length=1, max_length=60)],
    limit: Annotated[int, Query(ge=1, le=15)] = 15,
):
    """Получение списка общих тегов (Теги для квизов и статьей одинаковые).

    По умолчанию ограничен 15 тегами.
    """
    result = await get_tags(session, title_status, limit)
    if result is None:
        raise HTTPException(404, "По Вашему запросу ничего не найдено..")
    return result
