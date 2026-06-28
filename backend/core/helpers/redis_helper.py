from redis.asyncio import Redis
from redis.typing import ResponseT

from core.config import settings


class RedisHelper:
    """Async Redis helper for caching API responses.

    Manages a single Redis client instance for the lifetime of the application.
    Stores and retrieves JSON-serialized data with TTL support.
    """

    def __init__(self, url: str):
        self._url = url
        self._client = Redis.from_url(self._url)

    async def set(self, key: str, value: str, ex: int) -> ResponseT:
        return await self._client.set(name=key, value=value, ex=ex)

    async def get(self, key: str) -> ResponseT:
        return await self._client.get(name=key)

    async def delete(self, key: str) -> ResponseT:
        return await self._client.delete(key)

    async def close(self) -> None:
        await self._client.aclose()


redis_helper = RedisHelper(url=settings.redis.url)
