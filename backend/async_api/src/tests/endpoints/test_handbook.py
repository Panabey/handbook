import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.orm import insert_value

from modules.database.models import Handbook

pytestmark = pytest.mark.asyncio


async def test_get_handbook_all(client: AsyncClient, session: AsyncSession):
    # без заполнения информации
    resposne = await client.get(url="/api/v1/handbook/all")
    assert resposne.json() == []

    payload = {"title": "Python"}
    await insert_value(Handbook, session, **payload)

    resposne = await client.get(url="/api/v1/handbook/all")
    assert resposne.json() == [
        {
            "id": 1,
            "title": "Python",
            "description": None,
            "logo_url": None,
            "status": None,
        }
    ]


async def test_get_handbook_one(client: AsyncClient):
    # без заполнения информации
    resposne = await client.get(url="/api/v1/handbook/", params={"page_id": 1})
    assert resposne.status_code == 404


async def test_get_handbook_content(client: AsyncClient):
    # без заполнения информации
    resposne = await client.get(
        url="/api/v1/handbook/content", params={"handbook": "py"}
    )
    assert resposne.status_code == 404
