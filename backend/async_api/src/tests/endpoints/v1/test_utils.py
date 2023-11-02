import pytest

from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_favicon(client: AsyncClient):
    """Тестирование favicon на заголовки кеширования"""
    response = await client.get(url="/favicon.ico")
    assert response.status_code == 200

    headers = list(response.headers.keys())
    assert "etag" in headers
    assert "last-modified" in headers


async def test_healthcheck(client: AsyncClient):
    """Тестирование на доступность коечной точки для вычисления
    uptime данного сервиса
    """
    response = await client.head(url="api/v1/utils/healthcheck")
    assert response.status_code == 200
