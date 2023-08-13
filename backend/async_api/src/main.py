from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core.settings import settings
from routers.api.v1.router import router


app = FastAPI(
    debug=settings.DEBUG_MODE,
    title="Handbook API",
    version="0.1.0",
    default_response_class=ORJSONResponse,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=("*"),
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT"),
)
app.include_router(router, prefix="/api")
