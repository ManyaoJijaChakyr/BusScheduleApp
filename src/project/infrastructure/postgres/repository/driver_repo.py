from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, text
from sqlalchemy.exc import IntegrityError
from project.schemas.driver import DriverSchema, DriverCreateUpdateSchema
from project.infrastructure.postgres.models import Driver
from project.core.exceptions import DriverNotFound, DriverAlreadyExists
from typing import Type
from project.core.exceptions import CompanyAlreadyExists, CompanyNotFound

class DriverRepository:
    _collection: Type[Driver] = Driver

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_drivers(self, session: AsyncSession) -> list[DriverSchema]:
        query = select(self._collection)
        drivers = await session.scalars(query)
        return [DriverSchema.model_validate(obj=driver) for driver in drivers.all()]

    async def get_driver_by_passport_number(self, session: AsyncSession, passport_number: str) -> DriverSchema:
        query = select(self._collection).where(self._collection.passport_number == passport_number)
        driver = await session.scalar(query)
        if not driver:
            raise DriverNotFound(_passport_number=passport_number)
        return DriverSchema.model_validate(obj=driver)

    async def create_driver(self, session: AsyncSession, driver: DriverCreateUpdateSchema) -> DriverSchema:
        query = insert(self._collection).values(driver.dict()).returning(self._collection)
        try:
            created_driver = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise DriverAlreadyExists(passport_number=driver.passport_number)
        return DriverSchema.model_validate(obj=created_driver)

    async def update_driver(self, session: AsyncSession, passport_number: str, driver: DriverCreateUpdateSchema) -> DriverSchema:
        query = update(self._collection).where(self._collection.passport_number == passport_number).values(driver.dict()).returning(self._collection)
        updated_driver = await session.scalar(query)
        if not updated_driver:
            raise DriverNotFound(_passport_number=passport_number)
        return DriverSchema.model_validate(obj=updated_driver)

    async def delete_driver(self, session: AsyncSession, passport_number: str) -> None:
        query = delete(self._collection).where(self._collection.passport_number == passport_number)
        result = await session.execute(query)
        if not result.rowcount:
            raise DriverNotFound(_passport_number=passport_number)