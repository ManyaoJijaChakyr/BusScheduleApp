from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, text
from sqlalchemy.exc import IntegrityError
from project.schemas.stop import StopSchema, StopCreateUpdateSchema
from project.infrastructure.postgres.models import Stop
from project.core.exceptions import StopNotFound, StopAlreadyExists

class StopRepository:
    _collection: Type[Stop] = Stop

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_stops(self, session: AsyncSession) -> list[StopSchema]:
        query = select(self._collection)
        stops = await session.scalars(query)
        return [StopSchema.model_validate(obj=stop) for stop in stops.all()]

    async def get_stop_by_coords(self, session: AsyncSession, latitude: float, longitude: float) -> StopSchema:
        query = select(self._collection).where(self._collection.latitude == latitude, self._collection.longitude == longitude)
        stop = await session.scalar(query)
        if not stop:
            raise StopNotFound(_latitude=latitude, _longitude=longitude)
        return StopSchema.model_validate(obj=stop)

    async def create_stop(self, session: AsyncSession, stop: StopCreateUpdateSchema) -> StopSchema:
        query = insert(self._collection).values(stop.model_dump()).returning(self._collection)
        try:
            created_stop = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise StopAlreadyExists(latitude=stop.latitude, longitude=stop.longitude)
        return StopSchema.model_validate(obj=created_stop)

    async def update_stop(self, session: AsyncSession, latitude: float, longitude: float, stop: StopCreateUpdateSchema) -> StopSchema:
        query = update(self._collection).where(self._collection.latitude == latitude, self._collection.longitude == longitude).values(stop.model_dump()).returning(self._collection)
        updated_stop = await session.scalar(query)
        if not updated_stop:
            raise StopNotFound(_latitude=latitude, _longitude=longitude)
        return StopSchema.model_validate(obj=updated_stop)

    async def delete_stop(self, session: AsyncSession, latitude: float, longitude: float) -> None:
        query = delete(self._collection).where(self._collection.latitude == latitude, self._collection.longitude == longitude)
        result = await session.execute(query)
        if not result.rowcount:
            raise StopNotFound(_latitude=latitude, _longitude=longitude)