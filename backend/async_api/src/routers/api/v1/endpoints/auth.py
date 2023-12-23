from fastapi import APIRouter

from modules.oauth.clients import yandex_oauth
from modules.oauth.clients import AvailableService

router = APIRouter()


@router.get("/auth/yandex")
async def auth_via_yandex(code: str, state: str):
    # Запрос токена JWT от OAuth 2.0
    token_url = "https://oauth.yandex.ru/token"
    token = await yandex_oauth.fetch_token(token_url, code=code, state=state)
    access_token = token["access_token"]

    # Получение данных пользователя
    info_url = "https://login.yandex.ru/info"
    user_data = await yandex_oauth.get(
        info_url, headers={"Authorization": f"OAuth {access_token}"}
    )
    print(user_data.json())


@router.get("/login")
async def login_service(service: AvailableService):
    # Генерация строки авторизации для различный сервисов
    if service == service.YANDEX:
        auth_url = "https://oauth.yandex.ru/authorize"
        url, state = yandex_oauth.create_authorization_url(auth_url)
    return {"url": url, "service": service}
