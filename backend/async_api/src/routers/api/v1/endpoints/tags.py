from typing import Annotated

from fastapi import Query
from fastapi import Depends
from fastapi import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from routers.api.deps import get_async_session
from modules.database.orm.tags import get_tags

from modules.schemas.quiz import TagsDetail


router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_async_session)]


@router.get("/", response_model=list[TagsDetail])
async def get_all_tags(
    session: Session, limit: Annotated[int, Query(ge=1, le=15)] = 15
):
    """Получение списка общих тегов (Теги для квизов и статьей одинаковые).

    По умолчанию ограничен 15 тегами.
    """
    result = await get_tags(session, limit)
    return result
