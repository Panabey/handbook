import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils.orm import insert_value
from tests.utils.type import pydantic_datetime
from modules.database.models import (
    Handbook,
    HandbookContent,
    HandbookPage,
    HandBookStatus,
)

pytestmark = pytest.mark.asyncio


async def test_empty_handbook_all(client: AsyncClient):
    """Тестирование получения всех справочников, если тех
    нет в базе данных
    """
    resposne = await client.get(url="/api/v1/handbook/all")
    assert resposne.json() == []


async def test_handbook_all_without_status(client: AsyncClient, session: AsyncSession):
    """Тестирование получения всех справочников, если те
    НЕ имеют какого либо статуса и при этом присутсвуют в БД.
    """
    # Добавление справочника
    data = {"title": "Python", "is_visible": True}
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
    """Тестирование получения всех справочников, если те
    имеют какого либо статуса и при этом присутсвуют в БД.
    """
    # Добавление статуса для справочника
    data = {
        "title": "Дополняется",
        "color_text": "#ffffff",
        "color_background": "#000000",
    }
    status = await insert_value(HandBookStatus, session, None, **data)

    # Добавление справочника
    data = {"title": "Python", "status_id": status.id, "is_visible": True}
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
    """Тестирование получения содержимого справочника, если тот
    НЕ имеет содержимого
    """
    payload = {"handbook": "javascripts"}
    resposne = await client.get(url="/api/v1/handbook/content", params=payload)
    assert resposne.status_code == 404


async def test_handbook_content(client: AsyncClient, session: AsyncSession):
    """Тестирование получения содержимого справочника, если тот
    имеет содержимое
    """
    # Добавление справочника
    data = {"title": "JavaScripts", "is_visible": True}
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

    # Добавление раздела справочника
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
    """Тестирование получения содержимого страницы справочника, если такая
    НЕ существует в базе данных
    """
    resposne = await client.get(url="/api/v1/handbook/", params={"page_id": 1})
    assert resposne.status_code == 404


async def test_handbook_page(client: AsyncClient, session: AsyncSession):
    """Тестирование получения содержимого страницы справочника, если такая
    существует в базе данных
    """
    # Добавление справочника
    data = {"title": "Python", "is_visible": True}
    handbook = await insert_value(Handbook, session, Handbook, **data)

    # Добавление раздела справочника
    data = {
        "handbook_id": handbook.id,
        "title": "1. Основы",
        "description": "Empty",
    }
    content_id = await insert_value(
        HandbookContent, session, HandbookContent.id, **data
    )

    # Добавление страницы раздела
    data = {
        "content_id": content_id,
        "title": "Test",
        "short_description": "Test",
        "text": "Test",
        "reading_time": 1,
    }
    page = await insert_value(HandbookPage, session, HandbookPage, **data)

    resposne = await client.get(url="/api/v1/handbook/", params={"page_id": page.id})
    assert resposne.status_code == 200
    assert resposne.json() == {
        "id": page.id,
        "short_description": page.short_description,
        "title": page.title,
        "text": page.text,
        "reading_time": page.reading_time,
        "create_date": pydantic_datetime(page.create_date),
        "update_date": pydantic_datetime(page.update_date),
        "handbook": {"id": handbook.id, "title": handbook.title},
    }


async def test_empty_search_page(client: AsyncClient):
    """Тестирование поиска страниц по всем справочникам, которых
    НЕ существуют в базе данных
    """
    payload = {"q": "string", "limit": 15}
    resposne = await client.post(url="/api/v1/handbook/search", json=payload)
    assert resposne.status_code == 200
    assert resposne.json() == []


async def test_search_page(client: AsyncClient, session: AsyncSession):
    """Тестирование поиска страниц по всем справочникам, которых
    существуют в базе данных
    """
    # Добавление справочника
    data = {"title": "Python", "is_visible": True}
    handbook = await insert_value(Handbook, session, Handbook, **data)

    # Добавление раздела справочника
    data = {
        "handbook_id": handbook.id,
        "title": "1. Основы",
        "description": "Empty",
    }
    content_id = await insert_value(
        HandbookContent, session, HandbookContent.id, **data
    )
    # добавление несколько страниц
    list_page = []
    for i in range(2):
        data = {
            "content_id": content_id,
            "title": f"1.{i} Test page #{i}",
            "short_description": "Test",
            "text": "Test",
            "reading_time": 1,
        }
        page = await insert_value(HandbookPage, session, HandbookPage, **data)
        list_page.append(
            {
                "id": handbook.id,
                "title": handbook.title,
                "page_id": page.id,
                "page_title": page.title,
            }
        )
    # сортировка по id
    sorted(list_page, key=lambda x: x["page_id"])

    payload = {"q": "test page", "limit": 3}
    resposne = await client.post(url="/api/v1/handbook/search", json=payload)
    assert resposne.status_code == 200
    assert resposne.json() == list_page
