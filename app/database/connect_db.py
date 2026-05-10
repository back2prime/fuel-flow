from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


DATABASE_URL = "postgresql+asyncpg://postgres:12344321@127.0.0.1:5432/fuel_flow"

engine = create_async_engine(url=DATABASE_URL,pool_pre_ping=True)

session = async_sessionmaker(bind=engine,expire_on_commit=False)

async def get_session():
    async with session() as new_session:
        yield new_session




