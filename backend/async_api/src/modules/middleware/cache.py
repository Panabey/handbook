import re

from starlette.types import Send
from starlette.types import Scope
from starlette.types import Message
from starlette.types import Receive
from starlette.types import ASGIApp
from starlette.datastructures import Headers
from starlette.datastructures import MutableHeaders

from starlette.responses import Response


from modules.redis.utils import get_cache_content
from modules.redis.utils import set_cache_content


class RedisCacheMiddleware:
    def __init__(self, app: ASGIApp, include_path: dict[str, tuple[str, int]]) -> None:
        self.app = app
        self.header_name = "x-use-cache"
        self.include_path = include_path

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        # параметры кеширования
        cache_content = None
        allow_cache = False
        path = re.sub(r"/api/v\d+/", "", scope["path"])
        options = self.include_path.get(path)  # содержит (<ключ>, <ttl>)

        if options is not None:
            headers = Headers(scope=scope)
            if headers.get(self.header_name) == "true":
                # если запрошен контент из кеша
                allow_cache = True
                params = scope.get("query_string")

                redis_key = f"{options[0]}?{params.decode()}" if params else options[0]
                cache_content = await get_cache_content(redis_key)

        async def send_wrapper(message: Message) -> None:
            nonlocal allow_cache

            if message["type"] == "http.response.start" and allow_cache:
                if message["status"] != 200:
                    # разрешить кеширование если ответ правильно обработался
                    allow_cache = False
                else:
                    headers = MutableHeaders(scope=message)
                    headers.append("X-Cache-Status", "MISS")

            if message["type"] == "http.response.body" and allow_cache:
                # кеширование ответа
                await set_cache_content(redis_key, message["body"], options[1])

            await send(message)

        if cache_content is None:
            # выполнить стандартный запрос, так как данных в кеше нет
            await self.app(scope, receive, send_wrapper)
            return

        response = Response(
            cache_content,
            headers={"X-Cache-Status": "HIT"},
            media_type="application/json",
        )
        await response(scope, receive, send)
