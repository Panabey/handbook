from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine


from modules.database.models import Base

async_engine = create_async_engine("sqlite+aiosqlite:///handbook.db", echo=True)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def init_database() -> None:
    """Initial database initialization at startup
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
