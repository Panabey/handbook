from typing import Any, TypeVar

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


async def insert_value(
    table: T,
    session: AsyncSession,
    return_value: T | None = None,
    **kwargs: dict[str, Any]
) -> T:
    smt = insert(table).values(**kwargs)

    if return_value:
        smt = smt.returning(return_value)
        result = await session.execute(smt)
        await session.commit()
        return result.scalar()
    else:
        smt = smt.returning(table)
        result = await session.scalars(smt)
        await session.commit()
        return result.first()
