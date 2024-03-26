from typing import Any, TypeVar

from sqlalchemy import insert
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import InstrumentedAttribute

T = TypeVar("T", bound=DeclarativeBase)
ReturnValue = InstrumentedAttribute | type[T] | None


async def insert_value(
    table: type[T],
    session: AsyncSession,
    return_value: ReturnValue = None,
    **kwargs: Any
) -> T:
    smt = insert(table).values(**kwargs)

    if return_value:
        smt = smt.returning(return_value)
        result = await session.execute(smt)
        await session.commit()
        return result.scalar() # type: ignore
    else:
        smt = smt.returning(table)
        result = await session.scalars(smt)
        await session.commit()
        return result.first() # type: ignore
