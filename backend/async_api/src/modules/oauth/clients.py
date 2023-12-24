import orjson

from authlib.integrations.httpx_client import AsyncOAuth2Client

from core.settings import settings

from modules.schemas.auth import AvailableService


yandex_oauth = AsyncOAuth2Client(
    client_id=settings.YANDEX_CLIENT_ID,
    client_secret=settings.YANDEX_CLIENT_SECRET,
)

google_oauth = AsyncOAuth2Client(
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
)

github_oauth = AsyncOAuth2Client(
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
)


def generate_oauth_url(service_name: str):
    if service_name == AvailableService.YANDEX:
        auth_url = "https://oauth.yandex.ru/authorize"
        url, state = yandex_oauth.create_authorization_url(auth_url)
    elif service_name == AvailableService.GOOGLE:
        auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
        url, state = google_oauth.create_authorization_url(auth_url)
    elif service_name == AvailableService.GITHUB:
        auth_url = "https://github.com/login/oauth/authorize"
        url, state = github_oauth.create_authorization_url(auth_url)
    return url, state


async def get_user_yandex(code: str, state: str) -> dict:
    token_url = "https://oauth.yandex.ru/token"
    user_info_url = "https://login.yandex.ru/info"

    # Запрос токена
    token = await yandex_oauth.fetch_token(token_url, code=code, state=state)

    # Получение данных пользователя
    access_token = token["access_token"]
    response = await yandex_oauth.get(
        user_info_url, headers={"Authorization": f"OAuth {access_token}"}
    )
    return orjson.loads(response.content)


async def get_user_google(code: str, state: str) -> dict:
    token_url = "https://oauth2.googleapis.com/token"
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"

    # Запрос токена
    token = await google_oauth.fetch_token(token_url, code=code, state=state)

    # Получение данных пользователя
    access_token = token["access_token"]
    response = await google_oauth.get(
        user_info_url, headers={"Authorization": f"Bearer {access_token}"}
    )
    return orjson.loads(response.content)


async def get_user_github(code: str) -> dict:
    token_url = "https://github.com/login/oauth/access_token"
    user_info_url = "https://api.github.com/user"

    # Запрос токена
    token = await github_oauth.fetch_token(token_url, code=code)

    # Получение данных пользователя
    access_token = token["access_token"]
    response = await github_oauth.get(
        user_info_url, headers={"Authorization": f"Bearer {access_token}"}
    )
    user_data = orjson.loads(response.content)

    if user_data["email"] is None:
        # Если нет публичного email или он скрыт
        response_email = await github_oauth.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        emails = orjson.loads(response_email.content)

        for email_info in emails:
            if email_info["primary"]:
                # Заменить email в информации о пользователе
                user_data["email"] = email_info["email"]
                break
    return user_data
