from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
#from sqlalchemy import text
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.mechanic import MechanicSchema, MecCreateUpdateSchema
from project.infrastructure.postgres.models import Mechanic

#from project.core.config import settings
from project.core.exceptions import MecNotFound, MecAlreadyExists

class MechanicRepository:
    _collection: Type[Mechanic] = Mechanic

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_mecs(
        self,
        session: AsyncSession,
    ) -> list[MechanicSchema]:
        query = select(self._collection)

        mecs = await session.scalars(query)

        return [MechanicSchema.model_validate(obj=mec) for mec in mecs.all()]

    async def get_mec_by_p_n(
            self,
            session: AsyncSession,
            passport_number: str,
    ) -> MechanicSchema:
        query = (
            select(self._collection)
            .where(self._collection.passport_number == passport_number)
        )
        mec = await session.scalar(query)
        if not mec:
            raise MecNotFound(_passport_number=passport_number)
        return MechanicSchema.model_validate(obj=mec)

    async def create_mec(
            self,
            session: AsyncSession,
            mec: MecCreateUpdateSchema,
    ) -> MechanicSchema:
        query = (
            insert(self._collection)
            .values(mec.model_dump())
            .returning(self._collection)
        )
        try:
            created_mec = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise MecAlreadyExists(passport_number=mec.passport_number)
        return MechanicSchema.model_validate(obj=created_mec)

    async def update_mec(
            self,
            session: AsyncSession,
            passport_number: str,
            mec: MecCreateUpdateSchema,
    ) -> MechanicSchema:
        query = (
            update(self._collection)
            .where(self._collection.passport_number == passport_number)
            .values(mec.model_dump())
            .returning(self._collection)
        )
        updated_mec = await session.scalar(query)
        if not updated_mec:
            raise MecNotFound(_passport_number=passport_number)
        return MechanicSchema.model_validate(obj=updated_mec)

    async def delete_mec(
            self,
            session: AsyncSession,
            passport_number: str
    ) -> None:
        query = delete(self._collection).where(self._collection.passport_number == passport_number)
        result = await session.execute(query)
        if not result.rowcount:
            raise MecNotFound(_passport_number=passport_number)


