from typing import Annotated

from fastapi import Query
from fastapi import Depends
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from sqlalchemy.ext.asyncio import AsyncSession

from routers.api.deps import get_async_session

from modules.oauth.clients import generate_oauth_url
from modules.oauth.clients import get_user_yandex
from modules.oauth.clients import get_user_github

from modules.database.orm.user import create_user
from modules.database.orm.user import exists_user_info

from modules.schemas.auth import AvailableService

router = APIRouter()


Session = Annotated[AsyncSession, Depends(get_async_session)]


@router.get("/oauth/yandex")
async def auth_via_yandex(
    session: Session,
    code: Annotated[str, Query(max_length=1024)],
    state: Annotated[str, Query(max_length=1024)],
):
    # Получение данных от OAuth 2.0
    user_data = await get_user_yandex(code, state)

    # Проверка на сущестование пользователя в БД
    user_id = await exists_user_info(session, int(user_data["id"]), "yandex")
    if user_id is None:
        # Создание пользователя
        avatar_id = user_data["default_avatar_id"]
        payload = {
            "name": user_data["real_name"],
            "email": user_data["default_email"],
            "user_id": int(user_data["id"]),
            "avatar_url": f"https://avatars.yandex.net/get-yapic/{avatar_id}/islands-retina-50",
            "service_id": 1,
        }
        user_id = await create_user(session, **payload)
    return user_id


@router.get("/oauth/github")
async def auth_via_google(
    session: Session,
    code: Annotated[str, Query(max_length=1024)],
    state: Annotated[str, Query(max_length=1024)],
):
    # Получение данных от OAuth 2.0
    user_data = await get_user_github(code)

    # Проверка на сущестование пользователя в БД
    user_id = await exists_user_info(session, user_data["id"], "github")
    if user_id is None:
        # Создание пользователя
        payload = {
            "name": user_data["name"],
            "email": user_data["email"],
            "user_id": user_data["id"],
            "avatar_url": user_data["avatar_url"],
            "service_id": 2,
        }
        user_id = await create_user(session, **payload)
    return user_id


@router.get("/login")
def login_service(service: AvailableService):
    # Генерация строки авторизации для различный сервисов
    url, state = generate_oauth_url(service)
    return RedirectResponse(url)
