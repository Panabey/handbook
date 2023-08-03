from typing import Annotated

from fastapi import Depends
from fastapi import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from routers.api.deps import get_async_session
from modules.database.orm.posts import get_post

from modules.schemas.posts import PostDetail

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_async_session)]


@router.get("/all")
async def get_all_posts(session: Session):
    pass


@router.get("/", response_model=PostDetail)
async def get_page_post(session: Session, post_id: int):
    result = await get_post(session, post_id)
    return result
