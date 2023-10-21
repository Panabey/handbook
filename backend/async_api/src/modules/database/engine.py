from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from core.settings import settings

# На каждый запущенный экземпляр приложения будет запущено
# 15 подключений и 5 дополнительных в случае переполнения.
# Не рекомендуется увеличивать данный параметр до 100 активных подключений!
# Подробнее о pool: https://docs.sqlalchemy.org/en/20/core/pooling.html
async_engine = create_async_engine(
    settings.URL_DATABASE,
    pool_size=10,  # По умолчанию 5
    max_overflow=10,  # По умолчанию 10
    echo=settings.DEBUG_MODE,
)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)
