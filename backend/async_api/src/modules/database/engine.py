from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from core.settings import settings

async_engine = create_async_engine(settings.URL_DATABASE, echo=settings.DEBUG_MODE)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)
