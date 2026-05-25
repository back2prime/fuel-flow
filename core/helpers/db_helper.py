from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
    AsyncSession,
)

from core.config import settings


class DatabaseHelper:
    """Async database helper for managing SQLAlchemy engine and sessions.

    Creates and manages a single async engine and session factory
    for the lifetime of the application.
    """

    def __init__(self, url: str, echo: bool, pool_pre_ping: bool):
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            pool_pre_ping=pool_pre_ping,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, Any]:
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=settings.db.url, echo=settings.db.echo, pool_pre_ping=settings.db.pool_pre_ping
)
