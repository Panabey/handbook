from itsdangerous import URLSafeSerializer

from modules.database.engine import async_session
from core.settings import settings


async def get_async_session():
    async with async_session.begin() as session:
        yield session


async def set_session_cookie():
    return URLSafeSerializer(settings.SECRET_KEY, "auth")
