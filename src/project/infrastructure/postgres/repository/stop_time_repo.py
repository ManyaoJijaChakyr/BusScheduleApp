from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from project.schemas.stop_time import StopTimeSchema, StopTimeCreateUpdateSchema
from project.infrastructure.postgres.models import StopTime, Stop, Route
from project.core.exceptions import StopTimeNotFound, StopTimeAlreadyExists
from sqlalchemy.exc import IntegrityError

class StopTimeRepository:
    _collection: Type[StopTime] = StopTime

    async def get_all_stop_times(self, session: AsyncSession) -> list[StopTimeSchema]:
        query = select(self._collection)
        stop_times = await session.scalars(query)
        return [StopTimeSchema.model_validate(obj=stop_time) for stop_time in stop_times.all()]

    async def create_stop_time(self, session: AsyncSession, stop_time: StopTimeCreateUpdateSchema) -> StopTimeSchema:
        query = insert(self._collection).values(stop_time.dict()).returning(self._collection)
        try:
            created_stop_time = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise StopTimeAlreadyExists(longitude=stop_time.longitude, latitude=stop_time.latitude, route_number=stop_time.route_number)
        return StopTimeSchema.model_validate(obj=created_stop_time)


    async def delete_stop_time(self, session: AsyncSession, latitude: float, longitude: float, route_number: int) -> None:
        query = delete(self._collection).where(self._collection.latitude == latitude).where(self._collection.longitude == longitude).where(self._collection.route_number == route_number)
        result = await session.execute(query)
        if not result.rowcount:
            raise StopTimeNotFound(_stop_time=f"({latitude}, {longitude}, {route_number})")
