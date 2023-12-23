from typing import Annotated

from fastapi import Query
from fastapi import Cookie
from fastapi import Response
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import RedirectResponse

from modules.oauth.clients import yandex_oauth
from modules.oauth.clients import AvailableService

router = APIRouter()


@router.get("/auth/yandex")
async def auth_via_yandex(
    response: Response,
    code: str,
    state: Annotated[str, Query(max_length=1024)],
    oauth_state: Annotated[str, Cookie()],
):
    if state != oauth_state:
        raise HTTPException(400, "Значение state не совпадает!")

    # Удаление state значения
    response.delete_cookie(oauth_state)

    # Запрос токена JWT от OAuth 2.0
    token_url = "https://oauth.yandex.ru/token"
    token = await yandex_oauth.fetch_token(token_url, code=code, state=state)
    access_token = token["access_token"]

    # Получение данных пользователя
    info_url = "https://login.yandex.ru/info"
    user_data = await yandex_oauth.get(
        info_url, headers={"Authorization": f"OAuth {access_token}"}
    )
    return user_data.json()


@router.get("/login")
async def login_service(response: Response, service: AvailableService):
    # Генерация строки авторизации для различный сервисов
    state = None
    if service == service.YANDEX:
        auth_url = "https://oauth.yandex.ru/authorize"
        url, state = yandex_oauth.create_authorization_url(auth_url)

    # Сохранение state в cookie для проверки на подлинность
    response.set_cookie("oauth_state", state, max_age=600, httponly=True)
    return RedirectResponse(url)
