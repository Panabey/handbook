from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core.settings import settings
from routers.api.v1.router import router


app = FastAPI(
    debug=settings.DEBUG_MODE,
    title="Handbook API",
    version="0.5.2",
    default_response_class=ORJSONResponse,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_methods=("GET", "POST", "HEAD"),
)
app.include_router(router, prefix="/api")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")
