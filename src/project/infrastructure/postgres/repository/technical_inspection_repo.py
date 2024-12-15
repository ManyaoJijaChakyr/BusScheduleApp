from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError
from project.schemas.technical_inspection import TechnicalInspectionSchema, TechnicalInspectionCreateUpdateSchema
from project.infrastructure.postgres.models import TechnicalInspection
from project.core.exceptions import TechnicalInspectionNotFound, TechnicalInspectionAlreadyExists

class TechnicalInspectionRepository:
    _collection: Type[TechnicalInspection] = TechnicalInspection

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(query)
        return True if result else False

    async def get_all_inspections(self, session: AsyncSession) -> list[TechnicalInspectionSchema]:
        query = select(self._collection)
        inspections = await session.scalars(query)
        return [TechnicalInspectionSchema.model_validate(obj=inspection) for inspection in inspections]

    async def get_inspection_by_id(self, session: AsyncSession, inspection_id: int) -> TechnicalInspectionSchema:
        query = select(self._collection).where(self._collection.inspection_id == inspection_id)
        inspection = await session.scalar(query)
        if not inspection:
            raise TechnicalInspectionNotFound(_inspection_id=inspection_id)
        return TechnicalInspectionSchema.model_validate(obj=inspection)

    async def create_inspection(self, session: AsyncSession, inspection: TechnicalInspectionCreateUpdateSchema) -> TechnicalInspectionSchema:
        query = insert(self._collection).values(inspection.model_dump()).returning(self._collection)
        try:
            created_inspection = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise TechnicalInspectionAlreadyExists(inspection_id=inspection.inspection_id)
        return TechnicalInspectionSchema.model_validate(obj=created_inspection)

    async def update_inspection(self, session: AsyncSession, inspection_id: int, inspection: TechnicalInspectionCreateUpdateSchema) -> TechnicalInspectionSchema:
        query = update(self._collection).where(self._collection.inspection_id == inspection_id).values(inspection.model_dump()).returning(self._collection)
        updated_inspection = await session.scalar(query)
        if not updated_inspection:
            raise TechnicalInspectionNotFound(_inspection_id=inspection_id)
        return TechnicalInspectionSchema.model_validate(obj=updated_inspection)

    async def delete_inspection(self, session: AsyncSession, inspection_id: int) -> None:
        query = delete(self._collection).where(self._collection.inspection_id == inspection_id)
        result = await session.execute(query)
        if not result.rowcount:
            raise TechnicalInspectionNotFound(_inspection_id=inspection_id)
