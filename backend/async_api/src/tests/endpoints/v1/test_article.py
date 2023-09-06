import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils.orm import insert_value
from tests.utils.type import pydantic_datetime
from modules.database.models import Article

pytestmark = pytest.mark.asyncio


async def test_empty_all_articles(client: AsyncClient):
    payload = {"page": 1}
    resposne = await client.get(url="/api/v1/article/all", params=payload)
    assert resposne.status_code == 200
    assert resposne.json() == {
        "items": [],
        "current_page": 1,
        "total_page": 0,
    }


async def test_all_articles(client: AsyncClient, session: AsyncSession):
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
    payload = {"article_id": 100000}
    resposne = await client.get(url="/api/v1/article/", params=payload)
    assert resposne.status_code == 404


async def test_article(client: AsyncClient, session: AsyncSession):
    data = {"title": "test", "anons": "test", "text": "test", "reading_time": 1}
    article = await insert_value(Article, session, None, **data)

    payload = {"article_id": article.id}
    resposne = await client.get(url="/api/v1/article/", params=payload)
    assert resposne.status_code == 200
    assert resposne.json() == {
        "id": article.id,
        "title": article.title,
        "anons": article.anons,
        "text": article.text,
        "tags": [],
        "reading_time": article.reading_time,
        "create_date": pydantic_datetime(article.create_date),
        "update_date": pydantic_datetime(article.update_date),
    }


async def test_empty_search_article(client: AsyncClient):
    payload = {"q": "test"}
    resposne = await client.post(url="/api/v1/article/search", json=payload)
    assert resposne.status_code == 200
    assert resposne.json() == []


async def test_invalid_search_article(client: AsyncClient):
    payload = {"limit": 20}
    resposne = await client.post(url="/api/v1/article/search", json=payload)
    assert resposne.status_code == 400


async def test_search_article(client: AsyncClient, session: AsyncSession):
    data = {"title": "test", "anons": "test", "text": "test", "reading_time": 1}
    article = await insert_value(Article, session, None, **data)
    payload = {"q": article.title}

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
