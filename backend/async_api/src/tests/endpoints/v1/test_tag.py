import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils.orm import insert_value
from modules.database.models import TagStatus, Tag

pytestmark = pytest.mark.asyncio


async def test_empty_tags(client: AsyncClient):
    payload = {"status": "article"}
    resposne = await client.get(url="/api/v1/tags/", params=payload)
    assert resposne.status_code == 404


async def test_tags(client: AsyncClient, session: AsyncSession):
    data = {"title": "article"}
    tag_status = await insert_value(TagStatus, session, None, **data)

    data = {"title": "best practical", "status_id": tag_status.id}
    tag = await insert_value(Tag, session, None, **data)

    payload = {"status": "article"}
    resposne = await client.get(url="/api/v1/tags/", params=payload)
    assert resposne.status_code == 200
    assert resposne.json() == [
        {"id": tag.id, "title": tag.title},
    ]
