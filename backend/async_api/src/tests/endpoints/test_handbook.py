import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils.orm import insert_value
from modules.database.models import Handbook, HandbookContent, HandbookPage

pytestmark = pytest.mark.asyncio


async def test_get_handbook_all(client: AsyncClient, session: AsyncSession):
    # без заполнения информации
    resposne = await client.get(url="/api/v1/handbook/all")
    assert resposne.json() == []

    # добавление новой информации о справочнике
    payload = {"title": "Python"}
    handbook_id = await insert_value(Handbook, session, Handbook.id, **payload)

    resposne = await client.get(url="/api/v1/handbook/all")
    assert resposne.json() == [
        {
            "id": handbook_id,
            "title": "Python",
            "description": None,
            "logo_url": None,
            "status": None,
        }
    ]


async def test_get_handbook_content(client: AsyncClient, session: AsyncSession):
    # без заполнения информации
    parmas = {"handbook": "javascripts"}
    resposne = await client.get(url="/api/v1/handbook/content", params=parmas)
    assert resposne.status_code == 404

    # заполнение информации
    payload = {"title": "JavaScripts"}
    handbook_id = await insert_value(Handbook, session, Handbook.id, **payload)

    resposne = await client.get(url="/api/v1/handbook/content", params=parmas)
    assert resposne.status_code == 200
    assert resposne.json() == {
        "id": handbook_id,
        "title": "JavaScripts",
        "description": None,
        "content": [],
    }

    payload = {"handbook_id": handbook_id, "title": "1. Основы", "description": "Empty"}
    _ = await insert_value(HandbookContent, session, HandbookContent.id, **payload)

    resposne = await client.get(url="/api/v1/handbook/content", params=parmas)
    assert resposne.json() == {
        "id": handbook_id,
        "title": "JavaScripts",
        "description": None,
        "content": [{"title": "1. Основы", "description": "Empty", "page": []}],
    }


async def test_get_handbook_page(client: AsyncClient, session: AsyncSession):
    # без заполнения информации
    resposne = await client.get(url="/api/v1/handbook/", params={"page_id": 1})
    assert resposne.status_code == 404

    # заполнение информации
    payload = {"title": "Python"}
    handbook_id = await insert_value(Handbook, session, Handbook.id, **payload)

    payload = {"handbook_id": handbook_id, "title": "1. Основы", "description": "Empty"}
    content_id = await insert_value(
        HandbookContent, session, HandbookContent.id, **payload
    )

    payload = {
        "content_id": content_id,
        "title": "Test",
        "meta": "Test",
        "text": "Test",
        "reading_time": 1,
    }
    page_id = await insert_value(HandbookPage, session, HandbookPage.id, **payload)

    resposne = await client.get(url="/api/v1/handbook/", params={"page_id": page_id})
    assert resposne.status_code == 200
