from modules.database.engine import async_session


async def get_async_session():
    async with async_session.begin() as session:
        yield session
