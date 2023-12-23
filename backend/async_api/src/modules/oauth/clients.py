from enum import StrEnum
from authlib.integrations.httpx_client import AsyncOAuth2Client

from core.settings import settings


class AvailableService(StrEnum):
    YANDEX = "yandex"
    GOOGLE = "google"


yandex_oauth = AsyncOAuth2Client(
    client_id=settings.YANDEX_CLIENT_ID,
    client_secret=settings.YANDEX_CLIENT_SECRET,
)
