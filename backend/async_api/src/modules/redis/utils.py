from redis.asyncio import Redis

from core.settings import settings

client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1, protocol=3)


async def get_cache_content(key: str):
    return await client.get(key)


async def set_cache_content(key: str, value: str, expire: int = 3600):
    return await client.set(key, value, ex=expire)
