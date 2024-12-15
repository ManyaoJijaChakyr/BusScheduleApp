from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError
from project.schemas.trip import TripSchema, TripCreateUpdateSchema
from project.infrastructure.postgres.models import Trip
from project.core.exceptions import TripNotFound, TripAlreadyExists

class TripRepository:
    _collection: Type[Trip] = Trip

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(query)
        return True if result else False

    async def get_all_trips(self, session: AsyncSession) -> list[TripSchema]:
        query = select(self._collection)
        trips = await session.scalars(query)
        return [TripSchema.model_validate(obj=trip) for trip in trips]

    async def get_trip_by_id(self, session: AsyncSession, trip_id: int) -> TripSchema:
        query = select(self._collection).where(self._collection.trip_id == trip_id)
        trip = await session.scalar(query)
        if not trip:
            raise TripNotFound(_trip_id=trip_id)
        return TripSchema.model_validate(obj=trip)

    async def create_trip(self, session: AsyncSession, trip: TripCreateUpdateSchema) -> TripSchema:
        query = insert(self._collection).values(trip.model_dump()).returning(self._collection)
        try:
            created_trip = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise TripAlreadyExists(trip_id=trip.trip_id)
        return TripSchema.model_validate(obj=created_trip)

    async def update_trip(self, session: AsyncSession, trip_id: int, trip: TripCreateUpdateSchema) -> TripSchema:
        query = update(self._collection).where(self._collection.trip_id == trip_id).values(trip.model_dump()).returning(self._collection)
        updated_trip = await session.scalar(query)
        if not updated_trip:
            raise TripNotFound(_trip_id=trip_id)
        return TripSchema.model_validate(obj=updated_trip)

    async def delete_trip(self, session: AsyncSession, trip_id: int) -> None:
        query = delete(self._collection).where(self._collection.trip_id == trip_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise TripNotFound(_trip_id=trip_id)
