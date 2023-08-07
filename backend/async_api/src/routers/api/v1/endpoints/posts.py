from typing import Annotated

from fastapi import Query
from fastapi import Depends
from fastapi import APIRouter
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from routers.api.deps import get_async_session
from modules.database.orm.posts import get_post
from modules.database.orm.posts import search_post
from modules.database.orm.posts import get_all_post

from modules.schemas.base import DetailInfo
from modules.schemas.posts import PostDetail

router = APIRouter()

Int = Annotated[int, Query(ge=1, le=2147483647)]

Session = Annotated[AsyncSession, Depends(get_async_session)]


@router.get("/all")
async def get_all_posts(session: Session, continue_after: Int = None):
    result = await get_all_post(session, continue_after, 20)
    return result


@router.get("/", response_model=PostDetail, responses={
    404: {"model": DetailInfo}
})  # fmt: skip
async def get_page_post(session: Session, post_id: Int):
    result = await get_post(session, post_id)
    if result:
        return result
    raise HTTPException(404, "Данный пост не существует")


@router.get("/search")
async def get_search_post(
    session: Session,
    q: str,
    continue_after: Int,
):
    result = await search_post(session, q, continue_after, 20)
    return result
