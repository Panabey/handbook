from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.responses import ORJSONResponse

from modules.middleware.cache import RedisCacheMiddleware

from core.settings import settings
from routers.api.v1.router import router


app = FastAPI(
    debug=settings.DEBUG_MODE,
    title="Handbook API",
    version="1.4.0",
    description="Документация API проекта",
    default_response_class=ORJSONResponse,
    redirect_slashes=False,
    openapi_url=settings.OPEN_API_URL,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

# Используется только для кеширования контента
app.add_middleware(
    RedisCacheMiddleware,
    include_path={
        "handbook/all": ("hb:all", 3600),  # 1 час
        "handbook/content": ("hb:content", 1800),  # 30 минут
        "handbook": ("hb:page", 1800),
        "tags": ("tags", 10800),  # 3 часа
        "project/news/widget": ("project:news", 1800),
        "utils/sitemap": ("sitemap", 900),  # 15 минут
    },
)

app.include_router(router, prefix="/api")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")
