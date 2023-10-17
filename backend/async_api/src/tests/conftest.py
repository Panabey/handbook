import asyncio
import pytest
import pytest_asyncio

from httpx import AsyncClient
from sqlalchemy import delete

from modules.database.models import Base
from modules.database.engine import async_session, async_engine
from core.settings import settings

from main import app

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@192.168.1.3:5432/test_handbook"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_db_setup_sessionmaker() -> None:
    assert settings.URL_DATABASE == DATABASE_URL
    # всегда очищать и создавать тестовую БД между тестовыми сессиями
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(autouse=True)
async def session(test_db_setup_sessionmaker):
    async with async_session() as session:
        yield session

        # удалить все данные после теста
        for table in Base.metadata.tables.values():
            await session.execute(delete(table))
        await session.commit()


@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/") as client:
        yield client
