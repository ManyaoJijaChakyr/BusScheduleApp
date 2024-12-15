from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, text
from sqlalchemy.exc import IntegrityError
from project.schemas.route import RouteSchema, RouteCreateUpdateSchema
from project.infrastructure.postgres.models import Route
from project.core.exceptions import RouteNotFound, RouteAlreadyExists

class RouteRepository:
    _collection: Type[Route] = Route

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_routes(self, session: AsyncSession) -> list[RouteSchema]:
        query = select(self._collection)
        routes = await session.scalars(query)
        return [RouteSchema.model_validate(obj=route) for route in routes.all()]

    async def get_route_by_number(self, session: AsyncSession, route_number: int) -> RouteSchema:
        query = select(self._collection).where(self._collection.route_number == route_number)
        route = await session.scalar(query)
        if not route:
            raise RouteNotFound(_route_number=route_number)
        return RouteSchema.model_validate(obj=route)

    async def create_route(self, session: AsyncSession, route: RouteCreateUpdateSchema) -> RouteSchema:
        query = insert(self._collection).values(route.model_dump()).returning(self._collection)
        try:
            created_route = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise RouteAlreadyExists(route_number=route.route_number)
        return RouteSchema.model_validate(obj=created_route)

    async def update_route(self, session: AsyncSession, route_number: int, route: RouteCreateUpdateSchema) -> RouteSchema:
        query = update(self._collection).where(self._collection.route_number == route_number).values(route.model_dump()).returning(self._collection)
        updated_route = await session.scalar(query)
        if not updated_route:
            raise RouteNotFound(_route_number=route_number)
        return RouteSchema.model_validate(obj=updated_route)

    async def delete_route(self, session: AsyncSession, route_number: int) -> None:
        query = delete(self._collection).where(self._collection.route_number == route_number)
        result = await session.execute(query)
        if not result.rowcount:
            raise RouteNotFound(_route_number=route_number)