import pytest

from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_favicon(client: AsyncClient):
    resposne = await client.get(url="/favicon.ico")
    assert resposne.status_code == 200

    headers = list(resposne.headers.keys())
    assert "etag" in headers
    assert "last-modified" in headers


async def test_healthcheck(client: AsyncClient):
    resposne = await client.head(url="api/v1/utils/healthcheck")
    assert resposne.status_code == 200
