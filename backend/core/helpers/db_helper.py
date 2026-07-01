from typing import AsyncGenerator, Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
    AsyncSession,
)

from core.config import settings


class DatabaseHelper:
    """Database helper managing async and sync SQLAlchemy engines and session factories.

    Holds two engines (asyncpg for FastAPI, psycopg2 for Celery workers)
    and exposes corresponding session generators for use as dependencies.
    """

    def __init__(self, async_url: str, sync_url: str, echo: bool, pool_pre_ping: bool):
        self.async_engine: AsyncEngine = create_async_engine(
            url=async_url,
            echo=echo,
            pool_pre_ping=pool_pre_ping,
        )
        self.async_session_factory = async_sessionmaker(
            bind=self.async_engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )
        self.sync_engine = create_engine(
            url=sync_url, echo=echo, pool_pre_ping=pool_pre_ping
        )
        self.sync_session_factory = sessionmaker(
            bind=self.sync_engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, Any]:
        async with self.async_session_factory() as session:
            yield session

    def get_sync_session(self) -> Generator[Session, Any]:
        with self.sync_session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    async_url=settings.db.async_url,
    sync_url=settings.db.sync_url,
    echo=settings.db.echo,
    pool_pre_ping=settings.db.pool_pre_ping,
)