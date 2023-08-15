from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core.settings import settings
from routers.api.v1.router import router


app = FastAPI(
    debug=settings.DEBUG_MODE,
    title="Handbook API",
    version="0.2.1",
    default_response_class=ORJSONResponse,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=("GET", "POST", "HEAD"),
)
app.include_router(router, prefix="/api")
