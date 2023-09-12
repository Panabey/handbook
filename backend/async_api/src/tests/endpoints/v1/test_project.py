import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils.orm import insert_value
from tests.utils.type import pydantic_datetime
from modules.database.models import ProjectNews

pytestmark = pytest.mark.asyncio


async def test_empty_project_news(client: AsyncClient):
    payload = {"news_id": "9999"}
    resposne = await client.get(url="/api/v1/project/news/", params=payload)
    assert resposne.status_code == 404


async def test_project_news(client: AsyncClient, session: AsyncSession):
    data = {"title": "test_title", "text": "test_text", "reading_time": 1}
    project_news = await insert_value(ProjectNews, session, None, **data)

    payload = {"news_id": project_news.id}
    resposne = await client.get(url="/api/v1/project/news/", params=payload)
    assert resposne.status_code == 200
    assert resposne.json() == {
        "id": project_news.id,
        "title": project_news.title,
        "text": project_news.text,
        "reading_time": project_news.reading_time,
        "create_date": pydantic_datetime(project_news.create_date),
    }


async def test_all_news(client: AsyncClient, session: AsyncSession):
    data = {"title": "test_title", "text": "test_text", "reading_time": 1}
    project_news = await insert_value(ProjectNews, session, None, **data)

    payload = {"page": 1}
    resposne = await client.get(url="/api/v1/project/news/all", params=payload)
    assert resposne.status_code == 200
    assert resposne.json() == {
        "items": [
            {
                "id": project_news.id,
                "title": project_news.title,
                "reading_time": project_news.reading_time,
                "create_date": pydantic_datetime(project_news.create_date),
            }
        ],
        "current_page": 1,
        "total_page": 1,
    }


async def test_widget_news(client: AsyncClient, session: AsyncSession):
    data = {"title": "test_title", "text": "test_text", "reading_time": 1}
    project_news_1 = await insert_value(ProjectNews, session, None, **data)
    project_news_2 = await insert_value(ProjectNews, session, None, **data)

    resposne = await client.get(url="/api/v1/project/news/widget", params={"limit": 5})
    assert resposne.status_code == 200
    assert resposne.json() == [
        {
            "id": project_news_2.id,
            "title": project_news_2.title,
            "create_date": pydantic_datetime(project_news_2.create_date),
        },
        {
            "id": project_news_1.id,
            "title": project_news_1.title,
            "create_date": pydantic_datetime(project_news_1.create_date),
        },
    ]
