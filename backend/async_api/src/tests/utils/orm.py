from typing import Any

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSessionTransaction


async def insert_value(
    table: Any, transaction: AsyncSessionTransaction, **kwargs: dict[str, Any]
):
    smt = insert(table).values(**kwargs)
    await transaction.session.execute(smt)
    await transaction.session.commit()
