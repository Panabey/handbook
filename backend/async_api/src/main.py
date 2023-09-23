from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.responses import ORJSONResponse

from core.settings import settings
from routers.api.v1.router import router


app = FastAPI(
    debug=settings.DEBUG_MODE,
    title="Handbook API",
    version="0.9.3",
    default_response_class=ORJSONResponse,
    openapi_url=settings.OPEN_API_URL,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
)
app.include_router(router, prefix="/api")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")
