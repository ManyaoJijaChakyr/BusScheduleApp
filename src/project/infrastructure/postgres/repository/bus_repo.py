# project/repositories/bus_repo.py
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete, text
from sqlalchemy.exc import IntegrityError
from project.schemas.bus import BusSchema, BusCreateUpdateSchema
from project.infrastructure.postgres.models import Bus
from project.core.exceptions import BusNotFound, BusAlreadyExists

class BusRepository:
    _collection: Type[Bus] = Bus

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_buses(self, session: AsyncSession) -> list[BusSchema]:
        query = select(self._collection)
        buses = await session.scalars(query)
        return [BusSchema.model_validate(obj=bus) for bus in buses]

    async def get_bus_by_gos_num(self, session: AsyncSession, gos_num: str) -> BusSchema:
        query = select(self._collection).where(self._collection.gos_num == gos_num)
        bus = await session.scalar(query)
        if not bus:
            raise BusNotFound(_gos_num=gos_num)
        return BusSchema.model_validate(obj=bus)

    async def create_bus(self, session: AsyncSession, bus: BusCreateUpdateSchema) -> BusSchema:
        query = insert(self._collection).values(bus.model_dump()).returning(self._collection)
        try:
            created_bus = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise BusAlreadyExists(gos_num=bus.gos_num)
        return BusSchema.model_validate(obj=created_bus)

    async def update_bus(self, session: AsyncSession, gos_num: str, bus: BusCreateUpdateSchema) -> BusSchema:
        query = update(self._collection).where(self._collection.gos_num == gos_num).values(bus.model_dump()).returning(self._collection)
        updated_bus = await session.scalar(query)
        if not updated_bus:
            raise BusNotFound(_gos_num=gos_num)
        return BusSchema.model_validate(obj=updated_bus)

    async def delete_bus(self, session: AsyncSession, gos_num: str) -> None:
        query = delete(self._collection).where(self._collection.gos_num == gos_num)
        result = await session.execute(query)
        if not result.rowcount:
            raise BusNotFound(_gos_num=gos_num)
