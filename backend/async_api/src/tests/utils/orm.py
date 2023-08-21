from typing import Any

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession


async def insert_value(
    table: Any, session: AsyncSession, return_value: Any, **kwargs: dict[str, Any]
) -> Any:
    smt = insert(table).values(**kwargs).returning(return_value)
    result = await session.execute(smt)
    await session.commit()
    return result.scalar()
