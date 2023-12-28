from typing import Annotated

from fastapi import Path
from fastapi import Depends
from fastapi import APIRouter
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from routers.api.deps import get_async_session
from routers.api.deps import get_session_cookie

from modules.database.orm.user import get_user_account

from modules.schemas.base import DetailInfo
from modules.schemas.profile import MyProfileDetail
from modules.schemas.profile import AuthorProfileDetail

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_async_session)]
UserInfoCookie = Annotated[dict, Depends(get_session_cookie)]


@router.get(
    "/profile",
    response_model=MyProfileDetail,
    summary="Получение данных аккаунта пользователя",
    responses={
        401: {"model": DetailInfo},
        404: {"model": DetailInfo},
    },
)
async def my_profile(session: Session, user_info: UserInfoCookie):
    user = await get_user_account(session, user_info["user_id"])
    if user is None:
        raise HTTPException(404, "Пользователь не найден!")
    return user


@router.get(
    "/author/{user_id}",
    response_model=AuthorProfileDetail,
    summary="Получение данных любого пользователя",
    responses={400: {"model": DetailInfo}},
)
async def author_profile(
    session: Session, user_id: Annotated[int, Path(ge=1, le=2147483647)]
):
    user = await get_user_account(session, user_id, True)
    if user is None:
        raise HTTPException(404, "Пользователь не найден!")
    return user
