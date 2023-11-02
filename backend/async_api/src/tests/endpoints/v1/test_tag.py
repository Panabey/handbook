import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils.orm import insert_value
from modules.database.models import TagStatus, Tag

pytestmark = pytest.mark.asyncio


async def test_empty_tags(client: AsyncClient):
    """Тестирование получения тегов по названию группы, если тех
    НЕ существует в базе данных
    """
    payload = {"status": "article"}
    response = await client.get(url="/api/v1/tags", params=payload)
    assert response.status_code == 404


async def test_tags(client: AsyncClient, session: AsyncSession):
    """Тестирование получения тегов по названию группы, если те
    существуют в базе данных
    """
    # Добавление группы тегов
    data = {"title": "article"}
    tag_status = await insert_value(TagStatus, session, None, **data)

    # Добавление тегов
    list_tags = []
    for i in range(3):
        data = {"title": f"tag #{i}", "status_id": tag_status.id}
        tag = await insert_value(Tag, session, None, **data)
        list_tags.append({"id": tag.id, "title": tag.title})
    sorted(list_tags, key=lambda x: x["id"])

    payload = {"status": "article", "limit": 2}
    response = await client.get(url="/api/v1/tags", params=payload)
    assert response.status_code == 200
    assert response.json() == list_tags[:2]
