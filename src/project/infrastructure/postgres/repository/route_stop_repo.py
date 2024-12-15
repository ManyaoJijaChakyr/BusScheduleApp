
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from project.schemas.route_stop import RouteStopSchema, RouteStopCreateUpdateSchema
from project.infrastructure.postgres.models import RouteStop
from project.core.exceptions import RouteStopNotFound, RouteStopAlreadyExists
from typing import Type

class RouteStopRepository:
    _collection: Type[RouteStop] = RouteStop

    async def get_all_route_stops(self, session: AsyncSession) -> list[RouteStopSchema]:
        query = select(self._collection)
        route_stops = await session.scalars(query)
        return [RouteStopSchema.model_validate(obj=route_stop) for route_stop in route_stops.all()]

    async def create_route_stop(self, session: AsyncSession, route_stop: RouteStopCreateUpdateSchema) -> RouteStopSchema:
        query = insert(self._collection).values(route_stop.dict()).returning(self._collection)
        try:
            created_route_stop = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise RouteStopAlreadyExists(latitude=route_stop.latitude, longitude=route_stop.longitude, route_number=route_stop.route_number)
        return RouteStopSchema.model_validate(obj=created_route_stop)

    async def delete_route_stop(self, session: AsyncSession, latitude: float, longitude: float, route_number: int) -> None:
        query = delete(self._collection).where(self._collection.latitude == latitude).where(self._collection.longitude == longitude).where(self._collection.route_number == route_number)
        result = await session.execute(query)
        if not result.rowcount:
            raise RouteStopNotFound(_latitude=latitude, _longitude=longitude, _route_number=route_number)
