from contextlib import asynccontextmanager

from fastapi import FastAPI

from modules.database.engine import init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()
    yield

app = FastAPI(
    title="Handbook API",
    lifespan=lifespan
)


@app.get("/")
async def home():
    return b"test"
