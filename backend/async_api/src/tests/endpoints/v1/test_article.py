import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils.orm import insert_value
from tests.utils.type import pydantic_datetime
from modules.database.models import Article

pytestmark = pytest.mark.asyncio


async def test_empty_all_articles(client: AsyncClient):
    """Тестирование получения всех статей, если тех
    нет в базе данных
    """
    payload = {"page": 1}
    resposne = await client.get(url="/api/v1/article/all", params=payload)
    assert resposne.status_code == 200
    assert resposne.json() == {
        "items": [],
        "current_page": 1,
        "total_page": 0,
    }


async def test_all_articles(client: AsyncClient, session: AsyncSession):
    """Тестирование получения всех справочников, если тех
    есть в базе данных
    """
    # Добавление статьи
    data = {"title": "test", "anons": "test", "text": "test", "reading_time": 1}
    article = await insert_value(Article, session, None, **data)

    payload = {"page": 1}
    resposne = await client.get(url="/api/v1/article/all", params=payload)
    assert resposne.status_code == 200
    assert resposne.json() == {
        "items": [
            {
                "id": article.id,
                "logo_url": article.logo_url,
                "title": article.title,
                "anons": article.anons,
                "tags": [],
                "reading_time": article.reading_time,
                "create_date": pydantic_datetime(article.create_date),
            }
        ],
        "current_page": 1,
        "total_page": 1,
    }


async def test_empty_article(client: AsyncClient):
    """Тестирование получения конеркетной статьи, если той
    нет в базе данных
    """
    payload = {"article_id": 1}
    resposne = await client.get(url="/api/v1/article", params=payload)
    assert resposne.status_code == 404


async def test_article(client: AsyncClient, session: AsyncSession):
    """Тестирование получения конеркетной статьи, если та
    есть в базе данных
    """
    # Добавление статьи
    data = {
        "title": "test",
        "anons": "test",
        "text": "test",
        "reading_time": 1,
        "logo_url": "/media/1.png",
    }
    article = await insert_value(Article, session, None, **data)

    payload = {"article_id": article.id}
    resposne = await client.get(url="/api/v1/article", params=payload)
    assert resposne.status_code == 200
    assert resposne.json() == {
        "id": article.id,
        "logo_url": article.logo_url,
        "title": article.title,
        "anons": article.anons,
        "text": article.text,
        "tags": [],
        "reading_time": article.reading_time,
        "create_date": pydantic_datetime(article.create_date),
        "update_date": pydantic_datetime(article.update_date),
    }


async def test_empty_search_article(client: AsyncClient):
    """Тестирование поиска по названию статьи, если той
    не существует в базе данных
    """
    payload = {"q": "test", "tags": []}
    resposne = await client.post(url="/api/v1/article/search", json=payload)
    assert resposne.status_code == 200
    assert resposne.json() == []


async def test_invalid_search_article(client: AsyncClient):
    """Тестирование поиска по названию статьи, если не указан
    обязательный атрибут поиска по названию или тегу
    """
    payload = {"limit": 20, "tags": []}
    resposne = await client.post(url="/api/v1/article/search", json=payload)
    assert resposne.status_code == 400


async def test_search_article(client: AsyncClient, session: AsyncSession):
    """Тестирование поиска по названию статьи, если та
    существует в базе данных
    """
    # Добавление статьи для поиска
    data = {"title": "test", "anons": "test", "text": "test", "reading_time": 1}
    article = await insert_value(Article, session, None, **data)

    payload = {"q": article.title, "tags": []}
    resposne = await client.post(url="/api/v1/article/search", json=payload)
    assert resposne.status_code == 200
    assert resposne.json() == [
        {
            "id": article.id,
            "logo_url": article.logo_url,
            "title": article.title,
            "anons": article.anons,
            "tags": [],
            "reading_time": article.reading_time,
            "create_date": pydantic_datetime(article.create_date),
        }
    ]
