import os
import asyncio
import pytest
import pytest_asyncio

from httpx import AsyncClient

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from modules.database.models import Base

# изменения пути БД до инициализации приложения
DATABASE_URL = (
    "postgresql+asyncpg://postgres:postgres@192.168.1.3:5432/test_handbook"  # fmt: off
)
os.environ["URL_DATABASE"] = DATABASE_URL  # fmt: off

from main import app  # noqa: E402


test_engine = create_async_engine(DATABASE_URL, echo=True)
test_session = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_db_setup_sessionmaker() -> None:
    # always drop and create test db tables between tests session
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(autouse=True)
async def session(test_db_setup_sessionmaker):
    async with test_session().begin() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/") as client:
        yield client
