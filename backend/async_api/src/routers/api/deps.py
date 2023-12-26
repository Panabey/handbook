from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import APIKeyCookie
from fastapi.concurrency import run_in_threadpool

from itsdangerous import URLSafeSerializer
from itsdangerous.exc import BadSignature

from modules.database.engine import async_session
from core.settings import settings

session_cookie = APIKeyCookie(name="s", auto_error=False)


async def get_async_session():
    async with async_session.begin() as session:
        yield session


def set_session_cookie():
    return URLSafeSerializer(settings.SECRET_KEY, "auth")


async def get_session_cookie(session: Annotated[str, Depends(session_cookie)]) -> dict:
    if not session:
        raise HTTPException(401, "Токен некорректный и/или истёк!")

    serializer = URLSafeSerializer(settings.SECRET_KEY, "auth")
    try:
        user_data = await run_in_threadpool(serializer.loads, session)
    except BadSignature:
        raise HTTPException(401, "Токен некорректный и/или истёк!") from None
    return user_data
