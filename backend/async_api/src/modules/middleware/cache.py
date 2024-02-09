import re

from starlette.types import Send
from starlette.types import Scope
from starlette.types import Message
from starlette.types import Receive
from starlette.types import ASGIApp
from starlette.responses import Response
from starlette.datastructures import Headers
from starlette.datastructures import MutableHeaders

from modules.redis.utils import get_cache_content
from modules.redis.utils import set_cache_content


class RedisCacheMiddleware:
    """Промежуточное ПО для кеширования данных с использованием Redis."""

    __slots__ = ("app", "include_path", "header_name")

    def __init__(
        self,
        app: ASGIApp,
        include_path: dict[str, tuple[str, int]],
        header_name: str = "x-use-cache",
    ) -> None:
        """
        Инициализация промежуточного ПО.

        Args:
            app (`ASGIApp`): ASGI-приложение, к которому применяется промежуточное ПО.
            include_path (`dict`): Словарь путей, которые подлежат кешированию в \
            формате {<путь>: (<ключ>, <ttl>)}
        """
        self.app = app
        self.header_name = header_name
        self.include_path = include_path

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            # Если это не HTTP-запрос, передаем управление следующему промежуточному ПО
            await self.app(scope, receive, send)
            return

        # Извлекаем путь запроса и определяем, подлежит ли он кешированию
        path = re.sub(r"/api/v\d+/", "", scope["path"])
        options = self.include_path.get(path)

        if options is not None and Headers(scope=scope).get(self.header_name) == "true":
            params = scope.get("query_string")
            redis_key = f"{options[0]}:{params.decode()}" if params else options[0]

            # Получить данные из Redis
            cache_content = await get_cache_content(redis_key)
            allow_cache = True
        else:
            cache_content = None
            allow_cache = False

        async def send_wrapper(message: Message) -> None:
            nonlocal allow_cache

            if message["type"] == "http.response.start" and allow_cache:
                if message["status"] != 200:
                    # Запретить кеширование, если ответ неправильно обработался
                    allow_cache = False
                else:
                    headers = MutableHeaders(scope=message)
                    headers.append("X-Cache-Status", "MISS")
            elif message["type"] == "http.response.body" and allow_cache:
                # Кеширование ответа в Redis
                await set_cache_content(redis_key, message["body"], options[1])  # type: ignore

            await send(message)

        if cache_content is None:
            # Выполнить стандартный запрос, так как данных в кеше нет
            await self.app(scope, receive, send_wrapper)
            return

        # Выполнить запрос используя кешированные данные
        response = Response(
            cache_content,
            headers={"X-Cache-Status": "HIT"},
            media_type="application/json",
        )
        await response(scope, receive, send)
