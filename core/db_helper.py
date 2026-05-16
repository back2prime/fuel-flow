from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.config import db_settings


class DatabaseHelper:
    """Async database helper for managing SQLAlchemy engine and sessions.

    Creates and manages a single async engine and session factory
    for the lifetime of the application.
    """

    def __init__(self, url: str, echo: bool, pool_pre_ping: bool):
        self.engine = create_async_engine(
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


db_helper = DatabaseHelper(
    url=db_settings.url, echo=db_settings.echo, pool_pre_ping=db_settings.pool_pre_ping
)
