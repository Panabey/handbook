import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils.orm import insert_value
from tests.utils.type import pydantic_datetime
from modules.database.models import (
    Handbook,
    HandbookContent,
    HandbookPage,
    HandbookStatus,
    HandbookСategory,
)

pytestmark = pytest.mark.asyncio


async def test_empty_handbook_all(client: AsyncClient):
    """Тестирование получения всех справочников, если тех
    нет в базе данных
    """
    response = await client.get(url="/api/v1/handbook/all")
    assert response.json() == []


async def test_hidden_handbook(client: AsyncClient, session: AsyncSession):
    """Тестирование получения всех справочников, если те скрыты"""
    data = {"title": "Языки программирования"}
    category = await insert_value(HandbookСategory, session, None, **data)

    data = {"title": "Python", "is_visible": False, "category_id": category.id}
    _ = await insert_value(Handbook, session, None, **data)

    response = await client.get(url="/api/v1/handbook/all")
    assert response.status_code == 200
    assert response.json() == []


async def test_handbook_all_without_status(client: AsyncClient, session: AsyncSession):
    """Тестирование получения всех справочников, если те
    НЕ имеют какого либо статуса и при этом присутсвуют в БД.
    """
    data = {"title": "Языки программирования"}
    category = await insert_value(HandbookСategory, session, None, **data)

    data = {"title": "Python", "is_visible": True, "category_id": category.id}
    handbook = await insert_value(Handbook, session, None, **data)

    response = await client.get(url="/api/v1/handbook/all")
    assert response.json() == [
        {
            "title": category.title,
            "handbook": [
                {
                    "id": handbook.id,
                    "title": handbook.title,
                    "logo_url": handbook.logo_url,
                    "status": None,
                }
            ],
        }
    ]


async def test_handbook_all_with_status(client: AsyncClient, session: AsyncSession):
    """Тестирование получения всех справочников, если те
    имеют какого либо статуса и при этом присутсвуют в БД.
    """
    data = {"title": "Языки разметки"}
    category = await insert_value(HandbookСategory, session, None, **data)
    # Добавление статуса для справочника
    data = {
        "title": "Дополняется",
        "color_text": "#ffffff",
        "color_background": "#000000",
    }
    status = await insert_value(HandbookStatus, session, None, **data)

    # Добавление справочника
    data = {
        "title": "HTML",
        "status_id": status.id,
        "is_visible": True,
        "category_id": category.id,
    }
    handbook = await insert_value(Handbook, session, None, **data)

    response = await client.get(url="/api/v1/handbook/all")
    assert response.json() == [
        {
            "title": category.title,
            "handbook": [
                {
                    "id": handbook.id,
                    "title": handbook.title,
                    "logo_url": handbook.logo_url,
                    "status": {
                        "title": status.title,
                        "color_text": status.color_text,
                        "color_background": status.color_background,
                    },
                }
            ],
        }
    ]


async def test_handbook_empty_content(client: AsyncClient, session: AsyncSession):
    """Тестирование получения содержимого справочника, если тот
    НЕ имеет содержимого
    """
    payload = {"handbook": "javascripts"}
    response = await client.get(url="/api/v1/handbook/content", params=payload)
    assert response.status_code == 404


async def test_handbook_content(client: AsyncClient, session: AsyncSession):
    """Тестирование получения содержимого справочника, если тот
    имеет содержимое
    """
    data = {"title": "Языки программирования"}
    category = await insert_value(HandbookСategory, session, None, **data)

    data = {"title": "Python", "is_visible": True, "category_id": category.id}
    handbook = await insert_value(Handbook, session, None, **data)

    payload = {"handbook": "python"}
    response = await client.get(url="/api/v1/handbook/content", params=payload)
    assert response.status_code == 200
    assert response.json() == {
        "id": handbook.id,
        "title": handbook.title,
        "description": handbook.description,
        "content": [],
        "book": [],
    }

    # Добавление раздела справочника
    data = {
        "handbook_id": handbook.id,
        "title": "Основы",
        "description": "Empty",
        "part": 1,
    }
    content = await insert_value(HandbookContent, session, None, **data)

    response = await client.get(url="/api/v1/handbook/content", params=payload)
    assert response.status_code == 200
    assert response.json() == {
        "id": handbook.id,
        "title": handbook.title,
        "description": handbook.description,
        "content": [
            {
                "part": content.part,
                "title": content.title,
                "description": content.description,
                "page": [],
            }
        ],
        "book": [],
    }


async def test_emtpy_handbook_page(client: AsyncClient):
    """Тестирование получения содержимого страницы справочника, если такая
    НЕ существует в базе данных
    """
    response = await client.get(url="/api/v1/handbook", params={"page_id": 1})
    assert response.status_code == 404


async def test_handbook_page(client: AsyncClient, session: AsyncSession):
    """Тестирование получения содержимого страницы справочника, если такая
    существует в базе данных
    """
    data = {"title": "Языки программирования"}
    category = await insert_value(HandbookСategory, session, None, **data)

    data = {"title": "Python", "is_visible": True, "category_id": category.id}
    handbook = await insert_value(Handbook, session, Handbook, **data)

    data = {
        "handbook_id": handbook.id,
        "title": "Основы",
        "description": "empty",
        "part": 1,
    }
    content = await insert_value(HandbookContent, session, None, **data)

    # Добавление страницы раздела
    data = {
        "content_id": content.id,
        "title": "test",
        "short_description": "test",
        "subpart": 1,
        "text": "test",
        "reading_time": 1,
    }
    page = await insert_value(HandbookPage, session, HandbookPage, **data)

    response = await client.get(url="/api/v1/handbook", params={"page_id": page.id})
    assert response.status_code == 200
    assert response.json() == {
        "id": page.id,
        "short_description": page.short_description,
        "subpart": page.subpart,
        "title": page.title,
        "text": page.text,
        "reading_time": page.reading_time,
        "create_date": pydantic_datetime(page.create_date),
        "update_date": pydantic_datetime(page.update_date),
        "content": {
            "part": content.part,
            "handbook": {"id": handbook.id, "title": handbook.title},
        },
    }


async def test_empty_search_page(client: AsyncClient):
    """Тестирование поиска страниц по всем справочникам, которых
    НЕ существуют в базе данных
    """
    payload = {"q": "string", "limit": 15}
    response = await client.post(url="/api/v1/handbook/search", json=payload)
    assert response.status_code == 200
    assert response.json() == []


async def test_search_page(client: AsyncClient, session: AsyncSession):
    """Тестирование поиска страниц по всем справочникам, которых
    существуют в базе данных
    """
    data = {"title": "Языки программирования"}
    category = await insert_value(HandbookСategory, session, None, **data)

    data = {"title": "Python", "is_visible": True, "category_id": category.id}
    handbook = await insert_value(Handbook, session, Handbook, **data)

    # Добавление раздела справочника
    data = {
        "handbook_id": handbook.id,
        "title": "Основы",
        "description": "Empty",
        "part": 1,
    }
    content_id = await insert_value(
        HandbookContent, session, HandbookContent.id, **data
    )
    # добавление несколько страниц
    list_page = []
    for i in range(2):
        data = {
            "content_id": content_id,
            "title": f"Test page #{i}",
            "short_description": "Test",
            "text": "Test",
            "subpart": i,
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
    response = await client.post(url="/api/v1/handbook/search", json=payload)
    assert response.status_code == 200
    assert response.json() == list_page
