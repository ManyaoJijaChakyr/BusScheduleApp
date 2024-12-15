from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError
from project.schemas.repair_request import RepairRequestSchema, RepairRequestCreateUpdateSchema
from project.infrastructure.postgres.models import RepairRequest
from project.core.exceptions import RepairRequestNotFound, RepairRequestAlreadyExists

class RepairRequestRepository:
    _collection: Type[RepairRequest] = RepairRequest

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(query)
        return True if result else False

    async def get_all_requests(self, session: AsyncSession) -> list[RepairRequestSchema]:
        query = select(self._collection)
        requests = await session.scalars(query)
        return [RepairRequestSchema.model_validate(obj=req) for req in requests.all()]

    async def get_request_by_id(
            self,
            session: AsyncSession,
            request_id: int,
    ) -> RepairRequestSchema:
        query = (
            select(self._collection)
            .where(self._collection.request_id == request_id)
        )
        mec = await session.scalar(query)
        if not mec:
            raise RepairRequestNotFound(_request_id=request_id)
        return RepairRequestSchema.model_validate(obj=mec)

    async def create_request(self, session: AsyncSession, request: RepairRequestCreateUpdateSchema) -> RepairRequestSchema:
        query = insert(self._collection).values(request.model_dump()).returning(self._collection)
        try:
            created_request = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise RepairRequestAlreadyExists(request_id=request.request_id)
        return RepairRequestSchema.model_validate(obj=created_request)

    async def update_request(
            self,
            session: AsyncSession,
            request_id: int,
            mec: RepairRequestCreateUpdateSchema,
    ) -> RepairRequestSchema:
        query = (
            update(self._collection)
            .where(self._collection.request_id == request_id)
            .values(mec.model_dump())
            .returning(self._collection)
        )
        updated_mec = await session.scalar(query)
        if not updated_mec:
            raise RepairRequestNotFound(_request_id=request_id)
        return RepairRequestSchema.model_validate(obj=updated_mec)

    async def delete_request(self, session: AsyncSession, request_id: int) -> None:
        query = delete(self._collection).where(self._collection.request_id == request_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise RepairRequestNotFound(_request_id=request_id)