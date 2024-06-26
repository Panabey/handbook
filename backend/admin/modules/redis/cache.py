from redis import Redis
from core.settings import settings

client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=1,
    protocol=3,
    decode_responses=True,
)


def invalidate_pattern(
    pattern: str, count: int | None = None, _type: str | None = "STRING"
) -> None:
    """Удаление данных из Redis используя шаблон"""
    # Сложность поиска и удаления O(n)
    keys = client.scan(match=pattern, count=count, _type=_type)
    if keys[1]:
        # Удаление списка полученных ключей
        client.delete(*keys[1])
    del keys


def invalidate_key(key: str | list[str]) -> None:
    """Удаление данных из Redis используя ключ"""
    if isinstance(key, str):
        client.delete(key)
    else:
        # Если был получен список ключей
        client.delete(*key)
