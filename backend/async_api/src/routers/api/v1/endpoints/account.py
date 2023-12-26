from typing import Annotated

from fastapi import Depends
from fastapi import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from routers.api.deps import get_async_session
from routers.api.deps import get_session_cookie

from modules.database.orm.user import get_user_account

from modules.schemas.base import DetailInfo

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_async_session)]
UserInfoCookie = Annotated[dict, Depends(get_session_cookie)]


@router.get("/profile", responses={401: {"model": DetailInfo}})
async def my_profile(session: Session, user_info: UserInfoCookie):
    user = await get_user_account(session, user_info["user_id"])
    return user
