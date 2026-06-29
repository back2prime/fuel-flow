import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from typing import AsyncGenerator
from core.helpers.redis_helper import redis_helper, RedisHelper
from core.models.base import Base
from dotenv import load_dotenv
import os
from pathlib import Path
import asyncio
from app.main import app
from redis.asyncio import Redis
from core.helpers.db_helper import db_helper
from core.helpers.limiter import limiter

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv(Path(__file__).parent / ".env.test")

app.state.limiter = limiter
app.state.view_rate_limit = limiter._limiter

limiter.enabled = False

TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)


@pytest_asyncio.fixture(autouse=True)
async def reset_redis():
    redis_helper._client = Redis.from_url(redis_helper._url)
    yield
    await redis_helper._client.aclose()


@pytest_asyncio.fixture(scope="function", loop_scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    engine = create_async_engine(url=TEST_DATABASE_URL, echo=False)
    session_factory = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_session():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[db_helper.get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        follow_redirects=True,
    ) as ac:
        yield ac

    app.dependency_overrides.clear()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()
