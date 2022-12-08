from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from backuper.db.schema import Base, Model, Method, Subnet, DistinctDevice
from typing import Type


async def create_entry_from_dict(
        session: AsyncSession,
        model: Type[Base],
        params: dict
):
    obj = model(**params)
    session.add(obj)
    await session.commit()


async def create_entry_from_object(
        session: AsyncSession,
        obj: Base | list[Base]
):
    if isinstance(obj, list):
        for instance in obj:
            session.add(instance)
    else:
        session.add(obj)
    await session.commit()


async def get_all_entries(
        session: AsyncSession
):
    pass


async def get_entries_by_category(
        session: AsyncSession,
        model: Type[Base]
):
    pass


async def delete_all_entries(
        session: AsyncSession
):
    stmt = delete(Model)
    await session.execute(stmt)
    stmt = delete(Subnet)
    await session.execute(stmt)
    stmt = delete(DistinctDevice)
    await session.execute(stmt)
    stmt = delete(Method)
    await session.execute(stmt)


async def delete_entries_by_category(
        session: AsyncSession,
        model: Type[Base]
):
    pass
