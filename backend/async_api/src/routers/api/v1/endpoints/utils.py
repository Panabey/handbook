from typing import Annotated

from fastapi import Depends
from fastapi import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from routers.api.deps import get_async_session
from modules.database.orm.utils import sitemap_data

from modules.schemas.openapi import CACHE_HEADER
from modules.schemas.util import DetailSitemap

router = APIRouter()


@router.head(
    "/healthcheck",
    summary="Проверка работоспособности сервиса"
)  # fmt: skip
async def get_healthcheck():
    return None


@router.post(
    "/sitemap",
    response_model=DetailSitemap,
    openapi_extra=CACHE_HEADER,
    summary="Получение данных для генерации sitemap"
)  # fmt: skip
async def get_data_sitemap(
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    result = await sitemap_data(session)
    return result
