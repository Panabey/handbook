import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils.orm import insert_value
from modules.database.models import (
    Handbook,
    HandbookContent,
    HandbookPage,
    HandBookStatus,
)

pytestmark = pytest.mark.asyncio


async def test_empty_handbook_all(client: AsyncClient):
    resposne = await client.get(url="/api/v1/handbook/all")
    assert resposne.json() == []


async def test_handbook_all_without_status(client: AsyncClient, session: AsyncSession):
    data = {"title": "Python"}
    handbook_id = await insert_value(Handbook, session, Handbook.id, **data)

    resposne = await client.get(url="/api/v1/handbook/all")
    assert resposne.json() == [
        {
            "id": handbook_id,
            "title": "Python",
            "logo_url": None,
            "status": None,
        }
    ]


async def test_handbook_all_with_status(client: AsyncClient, session: AsyncSession):
    data = {
        "title": "Дополняется",
        "color_text": "#ffffff",
        "color_background": "#000000",
    }
    status = await insert_value(HandBookStatus, session, None, **data)

    data = {"title": "Python", "status_id": status.id}
    handbook_id = await insert_value(Handbook, session, Handbook.id, **data)

    resposne = await client.get(url="/api/v1/handbook/all")
    assert resposne.json() == [
        {
            "id": handbook_id,
            "title": "Python",
            "logo_url": None,
            "status": {
                "title": status.title,
                "color_text": status.color_text,
                "color_background": status.color_background,
            },
        }
    ]


async def test_handbook_empty_content(client: AsyncClient, session: AsyncSession):
    payload = {"handbook": "javascripts"}
    resposne = await client.get(url="/api/v1/handbook/content", params=payload)
    assert resposne.status_code == 404


async def test_handbook_content(client: AsyncClient, session: AsyncSession):
    data = {"title": "JavaScripts"}
    handbook = await insert_value(Handbook, session, None, **data)

    payload = {"handbook": "javascripts"}
    resposne = await client.get(url="/api/v1/handbook/content", params=payload)
    assert resposne.status_code == 200
    assert resposne.json() == {
        "id": handbook.id,
        "title": handbook.title,
        "description": handbook.description,
        "content": [],
    }

    data = {"handbook_id": handbook.id, "title": "1. Основы", "description": "Empty"}
    content = await insert_value(HandbookContent, session, None, **data)

    resposne = await client.get(url="/api/v1/handbook/content", params=payload)
    assert resposne.status_code == 200
    assert resposne.json() == {
        "id": handbook.id,
        "title": handbook.title,
        "description": handbook.description,
        "content": [
            {"title": content.title, "description": content.description, "page": []}
        ],
    }


async def test_emtpy_handbook_page(client: AsyncClient):
    resposne = await client.get(url="/api/v1/handbook/", params={"page_id": 1})
    assert resposne.status_code == 404


async def test_handbook_page(client: AsyncClient, session: AsyncSession):
    data = {"title": "Python"}
    handbook_id = await insert_value(Handbook, session, Handbook.id, **data)

    data = {
        "handbook_id": handbook_id,
        "title": "1. Основы",
        "description": "Empty",
    }
    content_id = await insert_value(
        HandbookContent, session, HandbookContent.id, **data
    )

    data = {
        "content_id": content_id,
        "title": "Test",
        "short_description": "Test",
        "text": "Test",
        "reading_time": 1,
    }
    page_id = await insert_value(HandbookPage, session, HandbookPage.id, **data)

    resposne = await client.get(url="/api/v1/handbook/", params={"page_id": page_id})
    assert resposne.status_code == 200


async def test_search_empty_page(client: AsyncClient):
    payload = {"q": "string", "limit": 15}
    resposne = await client.post(url="/api/v1/handbook/search", json=payload)
    assert resposne.status_code == 200
    assert resposne.json() == []
