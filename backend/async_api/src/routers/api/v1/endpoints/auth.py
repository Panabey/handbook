from typing import Annotated

from fastapi import Query
from fastapi import Cookie
from fastapi import Depends
from fastapi import Response
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.concurrency import run_in_threadpool

from itsdangerous import URLSafeSerializer
from sqlalchemy.ext.asyncio import AsyncSession

from routers.api.deps import get_async_session
from routers.api.deps import set_session_cookie

from modules.files.image import download_image_url

from modules.oauth.clients import get_user_yandex
from modules.oauth.clients import get_user_github
from modules.oauth.clients import generate_oauth_url

from modules.database.orm.user import create_user
from modules.database.orm.user import update_user
from modules.database.orm.user import exists_user_info

from modules.schemas.base import DetailInfo
from modules.schemas.auth import AvailableService

router = APIRouter()


Session = Annotated[AsyncSession, Depends(get_async_session)]
CookieSession = Annotated[URLSafeSerializer, Depends(set_session_cookie)]


@router.get(
    "/oauth/yandex",
    summary="Аутентификация через OAuth 2.0 Yandex",
    responses={
        200: {"model": DetailInfo},
        400: {"model": DetailInfo}
    }
)  # fmt: skip
async def auth_via_yandex(
    session: Session,
    serializer: CookieSession,
    response: Response,
    code: Annotated[str, Query(max_length=1024)],
    state: Annotated[str, Query(max_length=1024)],
    oauth_state: Annotated[str, Cookie(max_length=1024)],
):
    if oauth_state != state:
        raise HTTPException(400, "Значение state не совпадает!")

    response.delete_cookie("oauth_state")
    # Получение данных от OAuth 2.0
    user_data = await get_user_yandex(code, state)
    user_id_service = int(user_data["id"])

    # Получение изображения пользователя
    avatar_id = user_data["default_avatar_id"]
    avatar_url = f"https://avatars.yandex.net/get-yapic/{avatar_id}/islands-200"

    avatar_path, is_modif = await run_in_threadpool(
        download_image_url, avatar_url, f"a_{hex(user_id_service)[2:]}_{1}"
    )
    # Проверка на сущестование пользователя в БД
    user = await exists_user_info(session, user_id_service, "yandex")
    if user is None:
        # Создание пользователя
        payload = {
            "name": user_data["real_name"],
            "email": user_data["default_email"],
            "user_id": user_id_service,
            "avatar_url": avatar_path,
            "service_id": 1,
        }
        user = await create_user(session, **payload)

    if is_modif:
        await update_user(session, user.id, **{"avatar_url": avatar_path})

    # Создание сессии
    session_token = await run_in_threadpool(
        serializer.dumps, {"user_id": user.id, "service": "yandex"}
    )
    response.set_cookie("s", session_token, 365 * 24 * 60 * 60, httponly=True)
    return {"detail": "Добро пожаловать!"}


@router.get(
    "/oauth/github",
    summary="Аутентификация через OAuth 2.0 GitHub",
    responses={
        200: {"model": DetailInfo},
        400: {"model": DetailInfo}
    }
)  # fmt: skip
async def auth_via_github(
    session: Session,
    serializer: CookieSession,
    response: Response,
    code: Annotated[str, Query(max_length=1024)],
    state: Annotated[str, Query(max_length=1024)],
    oauth_state: Annotated[str, Cookie(max_length=1024)],
):
    if oauth_state != state:
        raise HTTPException(400, "Значение state не совпадает!")

    response.delete_cookie("oauth_state")
    # Получение данных от OAuth 2.0
    user_data = await get_user_github(code)
    user_id_service = int(user_data["id"])

    # Получение изображения пользователя
    avatar_url = user_data["avatar_url"]
    avatar_path, is_modif = await run_in_threadpool(
        download_image_url, avatar_url, f"a_{hex(user_id_service)[2:]}_{2}"
    )

    # Проверка на сущестование пользователя в БД
    user = await exists_user_info(session, user_id_service, "github")
    if user is None:
        # Создание пользователя
        payload = {
            "name": user_data["name"],
            "email": user_data["email"],
            "user_id": user_id_service,
            "avatar_url": avatar_path,
            "service_id": 2,
        }
        user = await create_user(session, **payload)

    if is_modif:
        await update_user(session, user.id, **{"avatar_url": avatar_path})

    # Создание сессии
    session_token = await run_in_threadpool(
        serializer.dumps, {"user_id": user.id, "service": "github"}
    )
    response.set_cookie("s", session_token, 365 * 24 * 60 * 60, httponly=True)
    return {"detail": "Добро пожаловать!"}


@router.get("/login", summary="Переадресация на нужный сервис OAuth 2.0")
def login_service(response: Response, service: AvailableService):
    # Генерация строки авторизации для различный сервисов
    url, state = generate_oauth_url(service)
    response = RedirectResponse(url)
    response.set_cookie("oauth_state", state, 3600, httponly=True)
    return response


@router.get(
    "/logout",
    summary="Выход из аккаунта",
    responses={200: {"model": DetailInfo}}
)  # fmt: skip
def logout_service(response: Response):
    response.delete_cookie("s")
    return {"detail": "Надеемся увидеть вас снова!"}
